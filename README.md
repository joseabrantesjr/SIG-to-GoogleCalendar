# SIG-to-GoogleCalendar

## Um script em python para pegar os horários de aula do SIG e converter para um arquivo .csv para ser usado no Google Agenda

[English Documentation](https://github.com/LimaEduardo/SIG-to-GoogleCalendar/tree/master/docs/englishDoc.md)

### Pré-requisitos

Você precisa de Python 3.x.x para rodar esse script

Para instalar as dependencias, digite no terminal

```
$ pip install -r requeriments.txt
```

### Rodando

Apenas rode no terminal

``` python3 sigToCalendar.py ```

Você vai precisar fornecer algumas informações para rodar o script

* Login - Seu login do SIG
* Password - Sua senha do SIG
* Start Date - A partir de qual dia você quer replicar seus horários
* End Date - Até que dia você quer replicar seus horários


Depois disso, o script irá gerar dois arquivos:

1. **.csv** - Para importar para o Google Calendar.
2. **.ics** - Para importar para o Calendar ou outros calendários compatíveis com o formato iCalendar (MacOS / IOS).

É fortemente recomendado criar uma nova agenda para importar o arquivo .csv

#### Como importar:

- **Google Calendar**:
  1. Acesse "calendar.google.com".
  2. Vá para "Importar > Selecionar um arquivo do seu computador".
  3. Escolha o arquivo `.csv` gerado.
  4. É fortemente recomendado criar uma nova agenda para importar o arquivo `.csv`.

- **Calendar**:
  1. Abra o arquivo `.ics` diretamente no seu dispositivo MacOS / IOS.
  2. O evento será automaticamente adicionado ao seu calendário.


### Contribuindo

Sinta-se a vontade para dar feedback, abrir novas issues e pull requests
