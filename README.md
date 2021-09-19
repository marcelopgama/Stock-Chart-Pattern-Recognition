# Stock-Chart-Pattern-Recognition

A identificação dos padrões em um gráfico de preço utilizada neste projeto consiste em comparar intervalos da série de dados com o padrão determinado.
Neste exemplo serão determinados os padrões V-Top e V-Bottom.

## 1- Primeiramente a série de dados é baixada do yahoo finance:

![image](https://user-images.githubusercontent.com/44553201/133943466-9bdc975e-abff-4953-8f9a-0c1a705c18a2.png)

## 2 - Determinação dos padrões:
#### Foi utilizada uma escala de 1 a 5, mas esta pode ser determinada pelo próprio usuário.

<div>
  <img src="https://user-images.githubusercontent.com/44553201/133943485-280112ca-6580-45b1-8cca-bb18b59146ad.png" >
  <img src="https://user-images.githubusercontent.com/44553201/133943785-30d9df0c-90a2-44e1-b8bf-be1cc7699497.png" >  
</div>

## 3 - Função para mudar a escala:
#### Como os preços não estão numa escala de 1 a 5 assim como os padrões, os dados não podem ser comparados. Então deve ser utilizada esta função para transformar os preços.
![image](https://user-images.githubusercontent.com/44553201/133943567-452595ca-c271-42ee-a103-b04f1ba9915e.png)

## 4 - R² para checar se o padrão existe:
#### Fazer um loop pelos dados e aplicando a função de transformação de escala em cada trecho. Após cada transformação, o vetor transformado e os vetores dos padrões são comparados utilizando R². Se o R² for maior que o grau de confiança escolhido significa que o naquele trecho de dados existe o padrão.
![image](https://user-images.githubusercontent.com/44553201/133943670-54457ce7-533c-47d0-9fb3-7d29831f5668.png)


