from .base import Bar
from time import sleep
from selenium.webdriver.common.by import By


class addProuct(Bar):
    '''oms->商品新增'''

    def iframe_page(self):
        '''进入商品新增ifrme'''
        # sleep(0.8)
        self.secondNavBar('商品新增').click()  # 进入系统时商品管理页面已显示
        self.driver.switch_to.frame(self.switchIframe('商品新增'))

    # 商品sku
    def proSku(self, sku):
        self.find_element(By.NAME, 'product_sku').send_keys(sku)

    # 商品名称
    def proName(self, name):
        self.find_element(By.NAME, 'product_name').send_keys(name)

    # 英文名称
    def englishName(self, enName):
        self.find_element(By.NAME, 'product_en_name').send_keys(enName)

    # 供应商代码
    def gysCode(self, code):
        self.find_element(By.NAME, 'supplier_code').send_keys(code)

    # 商品货号
    def proSpu(self, spu):
        self.find_element(By.NAME, 'product_spu').send_keys(spu)

    # 包装规格
    def packSpec(self, spec):
        self.find_element(By.NAME, 'pack_spec').send_keys(spec)

    # 申报价格
    def price(self, pri):
        self.find_element(By.NAME, 'price').send_keys(pri)

    # 商品净重
    def proWei(self, weight):
        self.find_element(By.NAME, 'net_weight').send_keys(weight)

    # 商品备注
    def note(self, notes):
        self.find_element(By.NAME, 'note').send_keys(notes)

    # 商品图片
    def image(self, imgSrc):
        self.find_element(By.NAME, 'product_images').send_keys(imgSrc)

    # 品牌
    def brand(self, bra):
        self.find_element(By.NAME, 'brand').send_keys(bra)

    # 生产厂家
    def manufactory(self, fac):
        self.find_element(By.NAME, 'manufactory').send_keys(fac)

    # 海关品名
    def hgName(self, name):
        self.find_element(By.NAME, 'hs_product_name').send_keys(name)

    # 规格型号
    def proSpec(self, spec):
        self.find_element(By.NAME, 'product_spec').send_keys(spec)

    # 国际编码
    def serialNo(self, num):
        self.find_element(By.NAME, 'serial_no').send_keys(num)

    # 体积
    def cube(self, cub):
        self.find_element(By.NAME, 'cube').send_keys(cub)

    # 商品链接
    def productLink(self, link):
        self.find_element(By.NAME, 'product_link').send_keys(link)

    # 商品毛重
    def grossWeight(self, weight):
        self.find_element(By.NAME, 'gross_weight').send_keys(weight)

    # textbox-prompt选择下拉选项后该class就会消失,可循环利用填写
    def prompts(self):
        loc = (By.CLASS_NAME, 'textbox-prompt')
        es = self.find_element(*loc)
        return es

    # 行邮税号
    def tax(self):
        self.prompts().click()
        self.driver.implicitly_wait(3)
        self.find_element(By.ID, '_easyui_combobox_i3_0').click()

    # 原产国
    def oriCountry(self):
        self.prompts().click()
        self.driver.implicitly_wait(3)
        self.find_element(By.ID, '_easyui_combobox_i4_0').click()

    # 海关编码
    def hgCode(self):
        self.find_element(By.CLASS_NAME, 'btn-default').click()
        self.find_element(By.ID, 'datagrid-row-r2-2-0').click()
        self.find_element(By.CLASS_NAME, 'panel-tool-close').click()

    # 保存按钮
    def save(self):
        self.find_element(By.CLASS_NAME, 'btn-success').click()

    # 商品添加统一入口
    def add_pro(self, proList):
        self.iframe_page()  # 进入商品新页面
        self.proSku(proList['product_sku'])
        self.proName(proList['product_name'])
        self.englishName(proList['product_en_name'])
        self.gysCode(proList['supplier_code'])
        self.proSpu(proList['product_spu'])
        self.packSpec(proList['pack_spec'])
        self.price(proList['price'])
        self.proWei(proList['net_weight'])
        self.note(proList['note'])
        self.image(proList['product_images'])
        self.brand(proList['brand'])
        self.manufactory(proList['manufactory'])
        self.hgName(proList['hs_product_name'])
        self.proSpec(proList['product_spec'])
        self.serialNo(proList['serial_no'])
        self.cube(proList['cube'])
        self.productLink(proList['product_link'])
        self.grossWeight(proList['gross_weight'])
        self.tax()
        self.oriCountry()
        self.hgCode()
        self.save()
