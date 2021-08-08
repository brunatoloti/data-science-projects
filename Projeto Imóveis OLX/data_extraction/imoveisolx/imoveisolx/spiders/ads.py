import scrapy


class AdsSpider(scrapy.Spider):
    name = 'ads'
    allowed_domains = ['olx.com.br']
    start_urls = ['https://ac.olx.com.br/imoveis/venda', 'https://ac.olx.com.br/imoveis/aluguel', 'https://al.olx.com.br/imoveis/venda', 'https://al.olx.com.br/imoveis/aluguel',
                  'https://ap.olx.com.br/imoveis/venda', 'https://ap.olx.com.br/imoveis/aluguel', 'https://am.olx.com.br/imoveis/venda', 'https://am.olx.com.br/imoveis/aluguel',
                  'https://ba.olx.com.br/imoveis/venda', 'https://ba.olx.com.br/imoveis/aluguel', 'https://ce.olx.com.br/imoveis/venda', 'https://ce.olx.com.br/imoveis/aluguel',
                  'https://df.olx.com.br/imoveis/venda', 'https://df.olx.com.br/imoveis/aluguel', 'https://es.olx.com.br/imoveis/venda', 'https://es.olx.com.br/imoveis/aluguel',
                  'https://go.olx.com.br/imoveis/venda', 'https://go.olx.com.br/imoveis/aluguel', 'https://ma.olx.com.br/imoveis/venda', 'https://ma.olx.com.br/imoveis/aluguel'
                  'https://mt.olx.com.br/imoveis/venda', 'https://mt.olx.com.br/imoveis/aluguel', 'https://ms.olx.com.br/imoveis/venda', 'https://ms.olx.com.br/imoveis/aluguel'
                  'https://mg.olx.com.br/imoveis/venda', 'https://mg.olx.com.br/imoveis/aluguel', 'https://pa.olx.com.br/imoveis/venda', 'https://pa.olx.com.br/imoveis/aluguel'
                  'https://pb.olx.com.br/imoveis/venda', 'https://pb.olx.com.br/imoveis/aluguel', 'https://pr.olx.com.br/imoveis/venda', 'https://pr.olx.com.br/imoveis/aluguel'
                  'https://pe.olx.com.br/imoveis/venda', 'https://pe.olx.com.br/imoveis/aluguel', 'https://pi.olx.com.br/imoveis/venda', 'https://pi.olx.com.br/imoveis/aluguel'
                  'https://rj.olx.com.br/imoveis/venda', 'https://rj.olx.com.br/imoveis/aluguel', 'https://rn.olx.com.br/imoveis/venda', 'https://rn.olx.com.br/imoveis/aluguel'
                  'https://rs.olx.com.br/imoveis/venda', 'https://rs.olx.com.br/imoveis/aluguel', 'https://ro.olx.com.br/imoveis/venda', 'https://ro.olx.com.br/imoveis/aluguel'
                  'https://rr.olx.com.br/imoveis/venda', 'https://rr.olx.com.br/imoveis/aluguel', 'https://sc.olx.com.br/imoveis/venda', 'https://sc.olx.com.br/imoveis/aluguel'
                  'https://sp.olx.com.br/imoveis/venda', 'https://sp.olx.com.br/imoveis/aluguel', 'https://se.olx.com.br/imoveis/venda', 'https://se.olx.com.br/imoveis/aluguel'
                  'https://to.olx.com.br/imoveis/venda', 'https://to.olx.com.br/imoveis/aluguel']

    def parse(self, response):
        ads_squares = response.xpath("//li[@class='sc-1fcmfeb-2 juiJqh']/a/@href").getall()
        for ad in ads_squares:
            yield scrapy.Request(url=ad, callback=self.parse_detail)
        # next_page = response.xpath('//a[@class="sc-1fvtocd-1 ijrAQg"]/@href')
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



