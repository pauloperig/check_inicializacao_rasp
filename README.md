# check_inicializacao_rasp
Check inicializacao raspberry pi e impressao do comprovante em impressora térmica 


Instruções

-Criar um serviço para execucao do script apos a inicializacao das placas de rede

sudo nano /etc/systemd/system/impressao-checklist.service

-Ativar o serviço

sudo systemctl daemon-reload
sudo systemctl enable impressao-checklist.service
