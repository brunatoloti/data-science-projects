import scrapy
from scrapy.crawler import CrawlerProcess


class AdsSpider(scrapy.Spider):
    name = 'to'
    allowed_domains = ['olx.com.br']
    start_urls = ['https://to.olx.com.br/imoveis/venda', 'https://to.olx.com.br/imoveis/aluguel']

    def parse(self, response):
        ads_squares = response.xpath("//ul[@class='sc-1fcmfeb-1 kntIvV']/li/a/@href").getall()
        for ad in ads_squares:
            yield scrapy.Request(url=ad, callback=self.parse_detail)
        next_page = response.xpath("//a[@data-lurker-detail='next_page']/@href")
        if next_page:
            yield scrapy.Request(url=next_page.extract_first(), callback=self.parse)

    def parse_detail(self, response):
        categoria = response.xpath(
            "//dt[contains(text(), 'Categoria')]/following-sibling::a/text()"
        ).extract_first()

        tipo = response.xpath(
            "//dt[contains(text(), 'Tipo')]/following-sibling::a/text()"
        ).extract_first()

        quartos = response.xpath(
            "//dt[contains(text(), 'Quartos')]/following-sibling::a/text()"
        ).extract_first()

        banheiros = response.xpath(
            "//dt[contains(text(), 'Banheiros')]/following-sibling::dd/text()"
        ).extract_first()

        vagas_garagem = response.xpath(
            "//dt[contains(text(), 'Vagas na garagem')]/following-sibling::dd/text()"
        ).extract_first()

        detalhes_imovel = response.xpath(
            "//dt[contains(text(), 'Detalhes do imóvel')]/following-sibling::dd/text()"
        ).extract_first()

        detalhes_condominio = response.xpath(
            "//dt[contains(text(), 'Detalhes do condominio')]/following-sibling::dd/text()"
        ).extract_first()

        cep = response.xpath(
            "//dt[contains(text(), 'CEP')]/following-sibling::dd/text()"
        ).extract_first()

        cidade = response.xpath(
            "//dt[contains(text(), 'Município')]/following-sibling::dd/text()"
        ).extract_first()

        url_anuncio = str(response.request.url)
        estado = url_anuncio.split('/')[2].split('.')[0].upper()

        bairro = response.xpath(
            "//dt[contains(text(), 'Bairro')]/following-sibling::dd/text()"
        ).extract_first()

        preco = response.xpath(
            "//h2[@class='sc-ifAKCX eQLrcK']/text()"
        ).extract_first()

        yield {
            'categoria': categoria,
            'tipo': tipo,
            'quartos': quartos,
            'banheiros': banheiros,
            'vagas_garagem': vagas_garagem,
            'detalhes_imovel': detalhes_imovel,
            'detalhes_condominio': detalhes_condominio,
            'cep': cep,
            'cidade': cidade,
            'estado': estado,
            'bairro': bairro,
            'preco': preco,
            'url': url_anuncio
        }

def run():
    process = CrawlerProcess({'FEED_EXPORT_ENCODING': 'UTF-8',
                              'FEED_URI': 'file:/c/Users/Admin/Documents/Data_Science/data-science-projects/projeto-imoveis-olx/data_extraction/imoveisolx/output/to_extract.json',
                              'CONCURRENT_REQUESTS': '55',
                              'DOWNLOAD_DELAY': '0.5',
                              'RANDOMIZE_DOWNLOAD_DELAY': False,
                              'COOKIES_ENABLED': False,
                              'LOG_LEVEL': 'INFO',
                              'USER_AGENT': [(
                                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
                              )]})
    process.crawl(AdsSpider)
    process.start()

if __name__ == '__main__':
    run()



