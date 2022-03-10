#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(data.table)
library(dplyr)
library(ggplot2)
library(plotly)
library(shinydashboard)
library(shinyWidgets)
library(geobr)
library(leaflet)


dados <- fread('/projeto-imoveis-olx/data_extraction/imoveisolx/output/dados_limpos.csv', encoding = 'UTF-8')
states <- read_state(year=2020)

cabecalho <- dashboardHeader(title = 'Dashboard Imóveis OLX')

barra_lateral <- dashboardSidebar(sidebarMenu(
    menuItem('Dashboard',
             tabName = 'dashboard',
             icon = icon('dashboard'),
             badgeLabel = '23 Dez 2021',
             badgeColor = 'blue'),
    menuItem('Filtros',
             tabName = 'filtros',
             icon = icon('filter'),
             awesomeCheckboxGroup(inputId = 'select_uf',
                                  label = 'Estados',
                                  choices = c('TODOS', unique(sort(dados$estado))),
                                  selected = 'TODOS',
                                  inline = TRUE),
             checkboxGroupInput(inputId = 'select_categoria',
                                label = 'Categoria',
                                choices = c('Todas', unique(sort(dados$categoria))),
                                selected = 'Todas', 
                                inline = TRUE),
             checkboxGroupInput(inputId = 'select_operacao',
                                label = 'Operação',
                                choices = c('Todas', unique(sort(dados$operacao))),
                                selected = 'Todas',
                                inline = TRUE),
             sliderInput(inputId = "range_price", 
                         label = "Preço",
                         min = 0, 
                         max = as.integer(max(dados$preco)), 
                         value = c(0,as.integer(max(dados$preco))),
                         round = TRUE))
))

painel_principal <- dashboardBody(
    tabItems(
        tabItem(tabName = 'dashboard',
                fluidRow(
                    valueBoxOutput(outputId = 'qtdads'),
                    valueBoxOutput(outputId = 'meanprice')
                ), #fim fluidrow
                h4(HTML('<b>Quantidade de anúncios por estado</b>')),
                fluidRow(
                    column(width = 12,
                           box(width = '100%',
                               leafletOutput(outputId = 'map', width = '100%'),
                               textOutput(outputId = 'descmapa')
                               )# fim box
                           )#fim column
                ),# fim fluidrow
                fluidRow(
                    column(width = 6,
                           h4(HTML('<b>Quantidade de anúncios por categoria</b>')),
                           box(width = '100%',
                               plotlyOutput(outputId = 'qtd_category')
                               )# fim box
                           ),#fim column
                    column(width = 6,
                           h4(HTML('<b>Quantidade de anúncios por operação</b>')),
                           box(width = '100%',
                               plotlyOutput(outputId = 'qtd_operation')
                               )#fim box
                           )# fim column
                ),#fim fluidrow
                fluidRow(
                    column(width = 12,
                           h4(HTML('<b>Quantidade de anúncios por tipo</b>')),
                           box(width = '100%',
                               plotlyOutput(outputId = 'qtd_type')
                               )# fim box
                           )# fim column
                ),#fim fluidrow
                fluidRow(
                    column(width = 6,
                           h4(HTML('<b>Quantidade de anúncios por número de quartos</b>')),
                           box(width = '100%',
                               plotlyOutput(outputId = 'qtd_bedrooms')
                               )#fim box
                           ),#fim column
                    column(width = 6,
                           h4(HTML('<b>Quantidade de anúncios por número de banheiros</b>')),
                           box(width = '100%',
                               plotlyOutput(outputId = 'qtd_bathrooms')
                               )# fim box
                           )#fim column
                ),# fim fluidrow
                fluidRow(
                    column(width = 12,
                           h4(HTML('<b>Quantidade de anúncios por número de vagas na garagem</b>')),
                            box(width = '100%',
                                plotlyOutput(outputId = 'parking_spaces')
                                )# fim box
                    )#fim column
                ),#fim fluidrow
                div(
                    id = 'message_to_show_more',
                    tags$hr(),
                    tags$h3('Clique no botão para ver mais. Isso pode levar alguns segundos.'),
                    actionButton('btn_show_more',
                                 paste0('Ver mais detalhes'),
                                 icon = icon('chevron-circle-down'))
                ),
                div(id = 'show_more_detail'),
                fluidRow(
                    column(width = 6,
                           uiOutput(outputId = 'title_preco_quartos'),
                           plotOutput(outputId = 'preco_quartos')
                    ),#fim column
                    column(width = 6,
                           uiOutput(outputId = 'title_preco_banheiros'),
                           plotOutput(outputId = 'preco_banheiros')
                    )
                ),#fim fluidrow
                fluidRow(
                    column(width = 12,
                           uiOutput(outputId = 'title_preco_vagas'),
                           plotOutput(outputId = 'preco_vagas')
                    )#fim column
                )#fim fluidrow
        ) # fim tabitem
    ) # fim tabitems
)

ui <- dashboardPage(header = cabecalho,
                    sidebar = barra_lateral,
                    body = painel_principal,
                    skin = 'blue')

server <- function(input, output, session) {
    
    dados_selecionados <- reactive({
        # filtro uf
        if (!'TODOS' %in% input$select_uf){
            dados <- dados %>% filter(estado %in% input$select_uf)
        }
        # filtro categoria
        if (!'Todas' %in% input$select_categoria){
            dados <- dados %>% filter(categoria %in% input$select_categoria)
        }
        # filtro operacao
        if (!'Todas' %in% input$select_operacao){
            dados <- dados %>% filter(operacao %in% input$select_operacao)
        }
        # filtro preco
        dados <- dados %>% filter(as.integer(preco) >= input$range_price[1] &
                                      as.integer(preco) <= input$range_price[2])
        dados
    })
    
    estados_frequencia <- data.frame(table(dados$estado)) %>%
        rename(estado = Var1, quantidade = Freq)
    estados <- dplyr::left_join(states, estados_frequencia, by = c("abbrev_state" = "estado"))
    pal <- colorNumeric(palette = 'Reds', domain = estados$quantidade)
    
    mapa_selecionados <- reactive({
        # filtro uf
        if (!'TODOS' %in% input$select_uf){
            states <- states %>% filter(abbrev_state %in% input$select_uf)
            estados_frequencia <- estados_frequencia %>% filter(estado %in% input$select_uf)
            estados <- dplyr::left_join(states, estados_frequencia, by = c("abbrev_state" = "estado"))
        }
        # filtro categoria
        if (!'Todas' %in% input$select_categoria){
            dados <- dados %>% filter(categoria %in% input$select_categoria)
            estados_frequencia <- data.frame(table(dados$estado)) %>%
                rename(estado = Var1, quantidade = Freq)
            estados <- dplyr::left_join(states, estados_frequencia, by = c("abbrev_state" = "estado"))
        }
        # filtro operacao
        if (!'Todas' %in% input$select_operacao){
            dados <- dados %>% filter(operacao %in% input$select_operacao)
            estados_frequencia <- data.frame(table(dados$estado)) %>%
                rename(estado = Var1, quantidade = Freq)
            estados <- dplyr::left_join(states, estados_frequencia, by = c("abbrev_state" = "estado"))
        }
        # filtro preco
        dados <- dados %>% filter(as.integer(preco) >= input$range_price[1] &
                                                   as.integer(preco) <= input$range_price[2])
        estados_frequencia <- data.frame(table(dados$estado)) %>%
            rename(estado = Var1, quantidade = Freq)
        estados <- dplyr::left_join(states, estados_frequencia, by = c("abbrev_state" = "estado"))
        
        estados
    })
    
    output$qtd_bedrooms <- renderPlotly({
        ggplotly(
            data.frame(table(dados_selecionados()$quartos)) %>%
                rename(quartos = Var1, qu = Freq) %>%
                ggplot(aes(text = paste('Número de quartos: ', quartos,
                                        '<br>Quantidade de anúncios: ', qu))) +
                geom_bar(aes(x = quartos, y = qu), stat = 'identity', fill = '#212D30') +
                ylab('Quantidade de anúncios') +
                xlab('Número de quartos') + 
                theme_bw(),
            tooltip = 'text'
        )
    })
    
    output$qtd_bathrooms <- renderPlotly({
        ggplotly(
            data.frame(table(dados_selecionados()$banheiros)) %>%
                rename(banheiros = Var1, b = Freq) %>%
                ggplot(aes(text = paste('Número de banheiros: ', banheiros,
                                        '<br>Quantidade de anúncios: ', b))) +
                geom_bar(aes(x = banheiros, y = b), stat = 'identity', fill = '#212D30') +
                ylab('Quantidade de anúncios') +
                xlab('Número de banheiros') + 
                theme_bw(),
            tooltip = 'text'
        )
    })
    
    output$parking_spaces <- renderPlotly({
        ggplotly(
            data.frame(table(dados_selecionados()$vagas_garagem)) %>%
                rename(vagas_garagem = Var1, vg = Freq) %>%
                ggplot(aes(text = paste('Vagas na garagem: ', vagas_garagem,
                                        '<br>Quantidade de anúncios: ', vg))) +
                geom_bar(aes(x = vagas_garagem, y = vg), stat = 'identity', fill = '#212D30') + 
                ylab('Quantidade de anúncios') +
                xlab('Número de vagas na garagem') + 
                theme_bw(),
            tooltip = 'text'
        )
    })
    
    output$qtd_type <- renderPlotly({
        ggplotly(
            data.frame(table(dados_selecionados()$tipo)) %>%
                rename(tipo = Var1, q = Freq) %>%
                ggplot(aes(x = reorder(tipo, q), y = q,
                           text = paste('Tipo: ', tipo,
                                        '<br>Quantidade de anúncios: ', q))) +
                geom_bar(stat = 'identity', fill = '#212D30') +
                coord_flip() + 
                ylab('Quantidade de anúncios') + 
                xlab('Tipo') + 
                theme_bw(),
            tooltip = 'text'
        )
    })
    
    output$qtd_category <- renderPlotly({
        ggplotly(
            data.frame(table(dados_selecionados()$categoria)) %>%
                rename(categoria = Var1, c = Freq) %>%
                ggplot(aes(text = paste('Categoria: ', categoria,
                                        '<br>Quantidade de anúncios: ', c))) +
                geom_bar(aes(x = categoria, y = c), stat = 'identity', fill = '#212D30') + 
                ylab('Quantidade de anúncios') +
                xlab('Categoria') +
                theme_bw(),
            tooltip = 'text'
        )
    })
    
    output$qtd_operation <- renderPlotly({
        ggplotly(
            data.frame(table(dados_selecionados()$operacao)) %>%
                rename(operacao = Var1, o = Freq) %>%
                ggplot(aes(text = paste('Operação: ', operacao,
                                        '<br>Quantidade de anúncios: ', o))) +
                geom_bar(aes(x = operacao, y = o), stat = 'identity', fill = '#212D30') +
                ylab('Quantidade de anúncios') +
                xlab('Operação') +
                theme_bw(),
            tooltip = 'text'
        )
    })
    
    output$map <- renderLeaflet({
        leaflet(mapa_selecionados()) %>% 
            addTiles() %>% 
            addPolygons(data = mapa_selecionados(),
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
                      title="Quantidade de anúncios",
                      pal = pal,
                      values = ~quantidade)
        
    })
    
    output$qtdads <- renderValueBox({
        valueBox(subtitle = 'Anúncios',
                 value = nrow(dados_selecionados()),
                 icon = icon('bars'),
                 color = 'blue')
    })
    
    output$meanprice <- renderValueBox({
        valueBox(subtitle = 'Média de preços',
                 value = round(mean(dados_selecionados()$preco), digits = 2),
                 icon = icon('dollar-sign'),
                 color = 'blue')
    })
    
    output$descmapa <- renderText({
        "Ao passar o cursor do mouse por cima do mapa, verá os nomes dos estados.
        Ao clicar em algum estado, verá a sua respectiva quantidade de anúncios."
    })
    
    observeEvent(input$btn_show_more,
                 {
                     removeUI(selector = '#btn_show_more')
                     removeUI(selector = '#message_to_show_more')
                     
                     output$title_preco_quartos <- renderUI({
                         h4(HTML('<b>Distribuição de preço por número de quartos</b>'))
                     })
                     output$preco_quartos <- renderPlot({
                         ggplot(dados_selecionados(), aes(x = quartos, y = preco)) +
                             geom_point(fill = '#212D30') +
                             xlab('Quantidade de quartos') +
                             ylab('Preço') +
                             theme_bw() +
                             theme(axis.title.x=element_text(size=15),
                                   axis.title.y=element_text(size=15),
                                   axis.text = element_text(size = 13))
                     })
                     output$title_preco_banheiros <- renderUI({
                         h4(HTML('<b>Distribuição de preço por número de banheiros</b>'))
                     })
                     output$preco_banheiros <- renderPlot({
                         ggplot(dados_selecionados(), aes(x = banheiros, y = preco)) +
                             geom_point(fill = '#212D30') +
                             xlab('Quantidade de banheiros') +
                             ylab('Preço') +
                             theme_bw() +
                             theme(axis.title.x=element_text(size=15),
                                   axis.title.y=element_text(size=15),
                                   axis.text = element_text(size = 13))
                     })
                     output$title_preco_vagas <- renderUI({
                         h4(HTML('<b>Distribuição de preço por número de vagas na garagem</b>'))
                     })
                     output$preco_vagas <- renderPlot({
                         ggplot(dados_selecionados(), aes(x = vagas_garagem, y = preco)) +
                             geom_point(fill = '#212D30') +
                             scale_x_continuous(limits = c(0, 10), breaks = seq(0, 10, by = 1)) +
                             xlab('Quantidade de vagas na garagem') +
                             ylab('Preço') +
                             theme_bw() +
                             theme(axis.title.x=element_text(size=15),
                                   axis.title.y=element_text(size=15),
                                   axis.text = element_text(size = 13))
                     })
                 })
}

# Run the application 
shinyApp(ui = ui, server = server)
