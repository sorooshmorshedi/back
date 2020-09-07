# Notes
* accounts which has method in Account model can't have floatAccount

# Naming
### Models
* relation: floatAccountGroup
* fields: postal_code
* methods: get_new_code

### Apps
* _* apps are add-on apps

### Default Accounts
* 1001 to 1999 ids are for dashtbashi module

# PDF Export Ubuntu Installation Commands
    wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz 
    tar vxf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
    sudo cp wkhtmltox/bin/wk* /usr/local/bin/
    sudo apt-get install libxrender1

# Notes

## Sanad
* after creating / updating sanad you should call `update_values` method to updating `sanad.bed` & `sanad.bes`
* `clearSanad` make sanad an empty manual sanad and it can be used by user again

## Imprest
* you should add imprest moein account to imprest default accounts
