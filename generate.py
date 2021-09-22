from lxml import etree

from utils import getValue, getCurDateXml

class Generate():

    def __init__(self, invoice, invoiceItems, invoiceExtra):
        self.invoice      = invoice
        self.invoiceItems = invoiceItems
        self.invoiceExtra = invoiceExtra if invoiceExtra is not None else list()
        self.addExtraItems()

    def addExtraItems(self):
        
        if self.invoice.get('cargo_free'):
            self.invoiceExtra.append({
                'name'     : 'Kargo Ücreti',
                'operator' : '+',
                'price'    : self.invoice.get('cargo_amount')
            })
        
        if self.invoiceExtra is not None:
            for item in self.invoiceExtra:
                if item.get('operator') == '+':
                    field = {
                        'product_name': item.get('name'),
                        'product_qty' : '1',
                        'tax'         : 0 if item.get('name') == 'Taksit Komisyonu' else 18,
                        'total'       : item.get('price'),
                        'extra'       : True
                    }
                    self.invoiceItems.append(field)
                else:
                    self.invoice.update({'fatura_isk': 1, 'fatura_isk_tutar': item.get('price')})

    def getXml(self, saveAs = False):

        # Root
        root = etree.Element('WFT')

        fieldsAyar = []

        # Ayar
        Ayar = etree.SubElement(root, 'AYAR')
        for key, value in fieldsAyar:
            etree.SubElement(Ayar, key).text = etree.CDATA(value)

        fieldsFatura = []

        # Fatura
        Fatura = etree.SubElement(root, 'FATURA')
        for key, value in fieldsFatura:
            etree.SubElement(Fatura, key).text = etree.CDATA(getValue(value, (True if key == 'E_MAIL' else False))) # Emailse Lower

        # Hareket
        FaturaHareket = etree.SubElement(root, 'FATURAHAREKET')

        for item in self.invoiceItems:

            fieldsItem = [
                ('BLSTKODU',   item.get('erp_id')),
                ('STOK_ADI',   item.get('product_name').replace('&', '-')),
                ('BIRIMI',     'ADET'),
                ('KDV_ORANI',  item.get('tax')),
                ('KPB_FIYATI', item.get('total')),
                ('KPBDVZ',     '1'),
                ('DEPO_ADI',   '' if item.get('extra') else 'MAGAZA DEPO')
            ]

            FaturaHareketItem = etree.SubElement(FaturaHareket, 'HAREKET')
            for key, value in fieldsItem:
                etree.SubElement(FaturaHareketItem, key).text = etree.CDATA(getValue(value))

        fieldsKapat = [
            ('ISLEM_TURU', '3'),
            ('KASA_ADI',   'WebConnect'),
            ('KPBDVZ',     '1'),
            ('KPB_ATUT',   str(self.invoice.get('total')))
        ]
            
        # Kapalı Fatura
        Kapat = etree.SubElement(root, 'KAPALIFATURA')

        if saveAs:
            with open('faturatmp.xml', 'wb') as f:
                f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8'))
                return True
        else:
            return etree.tostring(root, xml_declaration=True, encoding='utf-8').decode().replace("\n", "")