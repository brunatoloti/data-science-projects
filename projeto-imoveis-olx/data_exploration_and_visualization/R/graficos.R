# Amostra de dados - Imoveis OLX

# Importando as bibliotecas
library(data.table)
library(dplyr)
library(plotly)
install.packages("Rcpp")
library(Rcpp)
install.packages("sf")
library(sf)
install.packages("geobr")
library(geobr)
install.packages("gganimate")
library(gganimate)
install.packages("gifski")
library(gifski)
install.packages("leaflet")
library(leaflet)
library(htmltools)
install.packages("shinycssloaders")
library(shinycssloaders)

# Carregando a base de dados
dados <- fread('output/dados_limpos.csv', encoding = 'UTF-8')

# Verificando o resumo da base de dados
summary(dados)

grafico_quantidade_quartos <- ggplot(dados) + 
  geom_bar(aes(quartos), stat = 'count') +
  ylab('Quantidade de anúncios') +
  xlab('Número de quartos') + 
  theme_bw() +
  ggtitle('Quantidade de anúncios por número de quartos')
grafico_quantidade_quartos <- ggplotly(grafico_quantidade_quartos)
grafico_quantidade_quartos

grafico_quantidade_banheiros <- ggplot(dados) + 
  geom_bar(aes(banheiros), stat = 'count') +
  ylab('Quantidade de anúncios') +
  xlab('Número de banheiros') + 
  theme_bw() +
  ggtitle('Quantidade de anúncios por número de banheiros')
grafico_quantidade_banheiros <- ggplotly(grafico_quantidade_banheiros)
grafico_quantidade_banheiros

grafico_quantidade_vagas_garagem <- ggplot(dados) + 
  geom_bar(aes(vagas_garagem), stat = 'count') +
  ylab('Quantidade de anúncios') +
  xlab('Número de vagas na garagem') + 
  theme_bw() +
  ggtitle('Quantidade de anúncios por número de vagas na garagem')
grafico_quantidade_vagas_garagem <- ggplotly(grafico_quantidade_vagas_garagem)
grafico_quantidade_vagas_garagem

grafico_quantidade_tipo <- ggplot(dados) +
  geom_bar(aes(tipo), stat = 'count') +
  coord_flip() + 
  ylab('Quantidade de anúncios') + 
  xlab('Tipo') + 
  theme_bw() +
  ggtitle('Quantidade de anúncios por tipo')
grafico_quantidade_tipo <- ggplotly(grafico_quantidade_tipo)
grafico_quantidade_tipo

grafico_quantidade_uf <- data.frame(table(dados$estado)) %>%
  rename(estado = Var1, quantidade = Freq) %>%
  ggplot(aes(x = reorder(estado, quantidade), y = quantidade,
             text = paste('UF:', estado, '<br>', 'Qtd:', quantidade))) + 
  geom_bar(stat = 'identity') +
  coord_flip() +
  ylab('Quantidade de anúncios') +
  xlab('Estado') +
  theme_bw() +
  ggtitle('Quantidade de anúncios por estado')
grafico_quantidade_uf <- ggplotly(grafico_quantidade_uf, tooltip = 'text')
grafico_quantidade_uf

grafico_quantidade_categoria <- ggplot(dados) + 
  geom_bar(aes(categoria), stat = 'count') + 
  ylab('Quantidade de anúncios') +
  xlab('Categoria') +
  theme_bw() + 
  ggtitle('Quantidade de anúncios por categoria')
grafico_quantidade_categoria <- ggplotly(grafico_quantidade_categoria)
grafico_quantidade_categoria

grafico_operacao <- ggplot(dados) +
  geom_bar(aes(operacao), stat = 'count') +
  ylab('Quantidade de anúncios') +
  xlab('Operação') +
  theme_bw() +
  ggtitle('Quantidade de anúncios por operação')
grafico_operacao <- ggplotly(grafico_operacao)
grafico_operacao

states <- read_state(year=2020)
states
estados_frequencia <- data.frame(table(dados$estado)) %>%
  rename(estado = Var1, quantidade = Freq)
estados_frequencia
estados <- dplyr::left_join(states, estados_frequencia, by = c("abbrev_state" = "estado"))
mapa <- ggplot() +
  geom_sf(data = estados, aes(fill = quantidade), color = NA, size = .15) +
  geom_sf_text(data = estados, aes(label = abbrev_state, text = paste('UF:', abbrev_state, '<br>', 'Qtd:', quantidade)), colour = "white") +
  scale_fill_gradient(low = "grey", high = "black", name = 'Quantidade de anúncios') +
  ggtitle('Quantidade de anúncios por estado') +
  theme_bw() +
  theme(axis.title=element_blank(),
        axis.text=element_blank(),
        axis.ticks=element_blank())
mapa <- ggplotly(mapa, tooltip = 'text')
mapa


dados_states <- dplyr::left_join(states, dados, by = c("abbrev_state" = "estado"))
estados_frequencia <- data.frame(table(dados$estado)) %>%
  rename(estado = Var1, quantidade = Freq)
estados <- dplyr::left_join(states, estados_frequencia, by = c("abbrev_state" = "estado"))
pal <- colorNumeric(palette = 'Reds', domain = estados$quantidade)

sp_mapa <- leaflet(estados) %>% addTiles()
sp_mapa %>% addPolygons(data = estados,
                   smoothFactor = 0.5,
                   fillOpacity = 0.5,
                   weight = 0.5,
                   color = ~pal(quantidade),
                   opacity = 0.8,
                   highlightOptions = highlightOptions(color = 'black',
                                                       weight = 2,
                                                       bringToFront = TRUE),
                   popup = ~paste0(sep = ' ',
                                   '<b>Estado: </b>', abbrev_state, '<br>',
                                   '<b>Quantidade: </b>', quantidade),
                   label = ~abbrev_state) %>%
  addLegend("bottomright",
            title="Quantidade anúncios",
            pal = pal,
            values = ~quantidade)

preco_quartos <- ggplot(dados, aes(x = quartos, y = preco)) +
  geom_point() +
  xlab('Quantidade de quartos') +
  ylab('Preço') +
  theme_bw()
preco_quartos <- ggplotly(preco_quartos)
preco_quartos


preco_banheiros <- ggplot(dados, aes(x = banheiros, y = preco)) +
  geom_point() +
  xlab('Quantidade de banheiros') +
  ylab('Preço') +
  theme_bw()
preco_banheiros <- ggplotly(preco_banheiros)
preco_banheiros

preco_vagas <- ggplot(dados, aes(x = vagas_garagem, y = preco)) +
  geom_point() +
  scale_x_continuous(limits = c(0, 10), breaks = seq(0, 10, by = 1)) +
  xlab('Quantidade de vagas na garagem') +
  ylab('Preço') +
  theme_bw()
preco_vagas <- ggplotly(preco_vagas)
preco_vagas

teste <- ggplot(dados, aes(x = as.character(banheiros), y = preco, fill = as.character(banheiros))) + 
  geom_boxplot()

teste

estados_frequencia <- data.frame(table(dados$estado)) %>%
  rename(estado = Var1, quantidade = Freq)


dados_filtro_categoria <- dados %>% filter(categoria %in% c('Casas'))
estados_categoria_frequencia <- data.frame(table(dados_filtro_categoria$estado)) %>%
  rename(estado = Var1, quantidade = Freq)

estados <- dplyr::left_join(states, estados_frequencia, by = c("abbrev_state" = "estado"))
estados_filtro_categoria <- dplyr::left_join(states, estados_categoria_frequencia, by = c("abbrev_state" = "estado"))
