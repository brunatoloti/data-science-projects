#! /bin/sh

apt-get update && 
apt-get install r-base -y &&
apt-get install r-cran-plotly -y &&
apt-get install libudunits2-dev -y &&
apt-get install libgdal-dev -y &&
apt-get install libgeos-dev -y &&
apt-get install libproj-dev -y &&
Rscript /projeto-imoveis-olx/requirements.r &&
R -e "shiny::runApp('/projeto-imoveis-olx/data_exploration_and_visualization/app_imoveisolx', host='0.0.0.0', port=3838)"