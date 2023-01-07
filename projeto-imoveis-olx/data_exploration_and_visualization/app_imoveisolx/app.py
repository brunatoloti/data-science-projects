import pandas as pd
from shiny import App, render, ui, reactive
from shiny.ui import TagList, div, h3, h2, h1, head_content, tags
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# from sql.get_data import get_data


# imoveis = get_data()
imoveis = pd.read_csv('data_exploration_and_visualization/app_imoveisolx/imoveisolx.csv')


app_ui = ui.page_fluid(
    ui.tags.style(
        """
        .app-col {
            border-radius: 0px;
            background-color: rgb(128, 128, 128);
            padding: 20px;
            margin-top: 0px;
            margin-bottom: 5px;
            display: inherit;
        }
        .value-box {
            border-radius: 5px;
            background-color: rgb(128, 128, 128);
            padding: 20px;
            margin-top: 0px;
            margin-bottom: 5px;
            display: inherit;
        }
        .graphs {
            border-radius: 5px;
            background-color: rgb(224, 224, 224);
            padding: 20px;
            margin-top: 0px;
            margin-bottom: 5px;
            display: inherit;
        }
        """
    ),
    ui.row(
        ui.div(
            {"class": "app-col"},
            ui.h1(
                """
                Dashboard Imóveis
                """,
                style = "color: white; font-size: 30px; font-style: bold; margin-top: 0px; margin-left: 50px; margin-bottom: 0px;"
            )
        )
    ),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_selectize("select_estados", "Estados", {"todos": "Todos", "AC": "AC", "AL": "AL", "AM": "AM", "AP": "AP",
                                                          "BA": "BA", "CE": "CE", "DF": "DF", "ES": "ES", "GO": "GO", "MA": "MA",
                                                          "MG": "MG", "MS": "MS", "MT": "MT", "PA": "PA", "PB": "PB", "PE": "PE", "PI": "PI",
                                                          "PR": "PR", "RJ": "RJ", "RN": "RN", "RO": "RO", "RR": "RR", "RS": "RS",
                                                          "SC": "SC", "SE": "SE", "SP": "SP", "TO": "TO"},
                               multiple=True),
            ui.input_selectize("select_categoria", "Categoria", {"todas": "Todas", "Aluguel de quartos": "Aluguel de quartos",
                                                              "Apartamentos": "Apartamentos", "Casas": "Casas"},
                               multiple=True),
            ui.input_selectize("select_operacao", "Operação", {"todas": "Todas", "Aluguel": "Aluguel",
                                                            "Não informado": "Não informado", "Venda": "Venda"},
                               multiple=True),
            ui.input_slider("slider_preco", "Preço", min=int(min(imoveis.preco)), max=int(max(imoveis.preco)), value=[int(min(imoveis.preco)),int(max(imoveis.preco))])
        ),
        ui.panel_main(
            ui.row(
                ui.column(
                    6,
                    ui.div(
                        {"class": "value-box"},
                        ui.h1(
                            ui.output_text("qtd_ads"),
                            style="color: white;"
                        ),
                        ui.h6("""Quantidade de anúncios""", style="color: white;")
                    )
                ),
                ui.column(
                    6,
                    ui.div(
                        {"class": "value-box"},
                        ui.h1(
                            ui.output_text("mediana_precos"),
                            style="color: white;"
                        ),
                        ui.h6("""Mediana dos preços""", style="color: white;"),
                    )
                )
            ),
            ui.row(
                ui.column(
                    6,
                    ui.div(
                        {"class": "graphs"},
                        ui.output_plot("qtd_categoria")
                    )
                ),
                ui.column(
                    6,
                    ui.div(
                        {"class": "graphs"},
                        ui.output_plot("qtd_operacao")
                    )
                )
            ),
            ui.row(
                ui.column(
                    6,
                    ui.div(
                        {"class": "graphs"},
                        ui.output_plot("qtd_quartos")
                    )
                ),
                ui.column(
                    6,
                    ui.div(
                        {"class": "graphs"},
                        ui.output_plot("qtd_banheiros")
                    )
                )
            ),
            ui.row(
                ui.column(
                    12,
                    ui.div(
                        {"class": "graphs"},
                        ui.output_plot("qtd_garagem"),
                    )
                )
            )
        )
    )
)


def server(input, output, session):

    def dados_selecionados():
        imoveis = pd.read_csv('data_exploration_and_visualization/app_imoveisolx/imoveisolx.csv')
        if 'todos' not in str(input.select_estados()):
            imoveis['estado'] = imoveis['estado'].str.strip()
            imoveis = imoveis.query(f"estado in {str(input.select_estados())}")
        if 'todas' not in str(input.select_categoria()):
            imoveis['categoria'] = imoveis['categoria'].str.strip()
            imoveis = imoveis.query(f"categoria in {str(input.select_categoria())}")
        if 'todas' not in str(input.select_operacao()):
            imoveis['operacao'] = imoveis['operacao'].str.strip()
            imoveis = imoveis.query(f"operacao in {str(input.select_operacao())}")
        imoveis = imoveis.query(f"{input.slider_preco()[1]} >= preco >= {input.slider_preco()[0]}")
        
        return imoveis

    
    @output
    @render.text
    def qtd_ads():
        qtd = dados_selecionados().shape[0]
        return qtd


    @output
    @render.text
    def mediana_precos():
        mp = int(dados_selecionados()['preco'].median())
        return mp

    
    @output
    @render.plot
    def qtd_categoria():
        sns.set(rc={'axes.facecolor':(0,0,0,0), 'figure.facecolor':(0,0,0,0)})
        ax = sns.countplot(x=dados_selecionados()["categoria"], color='#212D30')
        ax.set_xlabel('Quantidade de categoria')
        ax.set_ylabel('Quantidade de anúncios')
        ax.set_title('Quantidade de anúncios por categoria')
        return ax

    
    @output
    @render.plot
    def qtd_operacao():
        sns.set(rc={'axes.facecolor':(0,0,0,0), 'figure.facecolor':(0,0,0,0)})
        ax = sns.countplot(x=dados_selecionados()["operacao"], color='#212D30')
        ax.set_xlabel('Quantidade de operacao')
        ax.set_ylabel('Quantidade de anúncios')
        ax.set_title('Quantidade de anúncios por operacao')
        return ax


    @output
    @render.plot
    def qtd_quartos():
        sns.set(rc={'axes.facecolor':(0,0,0,0), 'figure.facecolor':(0,0,0,0)})
        ax = sns.countplot(x=dados_selecionados()["quartos"], color='#212D30')
        ax.set_xlabel('Quantidade de quartos')
        ax.set_ylabel('Quantidade de anúncios')
        ax.set_title('Quantidade de anúncios por quantidade de quartos')
        return ax

    
    @output
    @render.plot
    def qtd_banheiros():
        sns.set(rc={'axes.facecolor':(0,0,0,0), 'figure.facecolor':(0,0,0,0)})
        ax = sns.countplot(x=dados_selecionados()["banheiros"], color='#212D30')
        ax.set_xlabel('Quantidade de banheiros')
        ax.set_ylabel('Quantidade de anúncios')
        ax.set_title('Quantidade de anúncios por quantidade de banheiros')
        return ax

    
    @output
    @render.plot
    def qtd_garagem():
        sns.set(rc={'axes.facecolor':(0,0,0,0), 'figure.facecolor':(0,0,0,0)})
        ax = sns.countplot(x=dados_selecionados()["vagas_garagem"], color='#212D30')
        ax.set_xlabel('Quantidade de vagas na garagem')
        ax.set_ylabel('Quantidade de anúncios')
        ax.set_title('Quantidade de anúncios por quantidade de vagas na garagem')
        return ax
       

    return ''


app = App(app_ui, server)