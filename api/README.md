# PSID-API

## It's time to develop ! 👨‍💻

The PSID (Property Sales Insights & Data) Project primarily aims to conduct in-depth statistical analysis on real estate sales data from the city of Madrid. The datasets have been preprocessed and cleaned to ensure their quality. This API is designed to respond to statistical queries issued by an Angular client, providing a smooth interface for data exploration.

Additionally, the PSID project has a secondary objective of developing and training predictive models from this data. This specific part of the project is detailed in another module called PSID-ML-API, where machine learning techniques will be implemented to provide predictive analyses and additional insights.

## Getting started  🏎

To make it easy for you to get started with this project, here's a list of recommended next steps.

- [INSTALL WSL DEBIAN](https://www.linuxfordevices.com/tutorials/linux/install-debian-on-windows-wsl)
- [INSTALL DOCKER](https://docs.docker.com/engine/install/debian/#install-from-a-package)
- [INSTALL MAKE](https://installati.one/debian/11/make/)
- [INSTALL PyCharm](https://www.jetbrains.com/help/pycharm/installation-guide.html)

## Clone project  🧬

    Create this tree project and clone the project : 

```
    - cd && mkdir psid-project && cd psid-project && git clone https://gitlab.com/psid-project/psid-api.git
```

## Define git global information    👀

    Change these lines, adding your personal informations (git information): 

```    
    git config --global user.email "gitlab-email" \
         &&  git config --global user.name "gitlab-name"

```

## Start project    🏁
#### Always run these commands to start the project : 

```
    sudo service docker start
```
AND

```
    make install
    make start
```