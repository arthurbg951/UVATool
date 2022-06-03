clear
clc
//----------------SUB-ROTINAS------------------------
//######################################################
//Interpolação de Lagrange
function y=lagrange()
n = input('Digite a quantidade de dados: ')
m(1:n,1:2) = 0
mdados = x_matrix('Dados ', m)
x = input('Valor de x para interpolar: ')
vx = mdados(1:n, 1)
vy = mdados(1:n , 2)
//processamento
for i=1:n
    num = 1
    den = 1
    xi = vx(i)
    for j = 1:n
        if(j<>i)
            num = num * (x - vx(j))
            den = den * (xi - vx(j))
        end
    end 
    L(i) = num/den
end
soma = 0
for i=1:n
    soma = soma + L(i)*vy(i)
end
y = soma
endfunction



//######################################################
//Regressão Linear
function [a,b,erro]=reglinear()
//Entrada de dados
n = input('Digite a quantidade de dados: ')
m(1:n,1:2) = 0
mdados = x_matrix('Dados ', m)
vx = mdados(1:n,1)
vy = mdados(1:n,2)
//Calculando os somatórios
sx = 0
sx2 = 0
sxy =0
sy = 0
for i=1:n
    sx = sx + vx(i)
    sx2 = sx2 + (vx(i))^2
    sy = sy + vy(i)
    sxy = sxy +vx(i)*vy(i)
end
//Preenchendo a matriz e vetor do sistema e resolvendo ...
ma(1,1) = sx2
ma(1,2) = sx
ma(2,1) = sx
ma(2,2) = n
vb(1) = sxy
vb(2) = sy
x = inv(ma) * vb
a = x(1)
b = x(2)
//Preenchendo vetor y calculado
for i=1:n 
    vyc(i) = a*vx(i) + b
end
//Calculando o somatório do erro ao quadrado
seq= 0
for i=1:n
    seq = seq + (vyc(i)-vy(i))^2
end
erro = seq
//Grafico
clf()
plot2d(vx,vy,-4)
plot2d(vx,vyc,2)
endfunction

//########################################################



//######################################################
//Regressão Exponencial
function [a,b,erro]=rege()
//Entrada de dados
n = input('Digite a quantidade de dados: ')
m(1:n,1:2) = 0
mdados = x_matrix('Dados ', m)
vx = mdados(1:n,1)
vy = mdados(1:n,2)
vyl = mdados(1:n,2)
for i=1:n
    vyl(i) = log(vy(i))
end
//Calculando os somatórios
sx = 0
sx2 = 0
sxy =0
sy = 0
for i=1:n
    sx = sx + vx(i)
    sx2 = sx2 + (vx(i))^2
    sy = sy + vyl(i)
    sxy = sxy +vx(i)*vyl(i)
end
//Preenchendo a matriz e vetor do sistema e resolvendo ...
ma(1,1) = sx2
ma(1,2) = sx
ma(2,1) = sx
ma(2,2) = n
vb(1) = sxy
vb(2) = sy
x = (inv(ma)) * vb
a = x(1)
b = x(2)
b = exp(b)
//Preenchendo vetor y calculado
for i=1:n 
    vyc(i) = b*exp(a*vx(i))
end
//Calculando o somatório do erro ao quadrado
seq= 0
for i=1:n
    seq = seq + (vyc(i)-vy(i))^2
end
erro = seq
//Grafico
clf()
plot2d(vx,vy,-4)
plot2d(vx,vyc,2)
endfunction

//########################################################



//######################################################
//Regressão Potencial
function [a,b,erro]=regp()
//Entrada de dados
n = input('Digite a quantidade de dados: ')
m(1:n,1:2) = 0
mdados = x_matrix('Dados ', m)
vx = mdados(1:n,1)
vy = mdados(1:n,2)
for i=1:n
    vyl(i)=log(vy(i))
    vxl(i)=log(vx(i))
end
//Calculando os somatórios
sx = 0
sx2 = 0
sxy =0
sy = 0
for i=1:n
    sx=sx+vxl(i)
    sx2=sx2+vxl(i)^2
    sy=sy+vyl(i)
    sxy=sxy+vxl(i)*vyl(i)
end
//Preenchendo a matriz e vetor do sistema e resolvendo ...
ma(1,1) = sx2
ma(1,2) = sx
ma(2,1) = sx
ma(2,2) = n
vb(1) = sxy
vb(2) = sy
x = inv(ma) * vb
a = x(1)
b = x(2)
b = exp(b)
//Preenchendo vetor y calculado
for i=1:n 
    vyc(i)=b*vx(i)^a
end
//Calculando o somatório do erro ao quadrado
seq= 0
for i=1:n
    seq = seq+(vyc(i)- vy(i))^2
end
erro = seq
//Grafico
clf()
plot2d(vx,vy,-4)
plot2d(vx,vyc,2)
endfunction

//########################################################


//######################################################
//Regressão Quadrática
function [a,b,c,erro]=regq()
//Entrada de dados
n = input('Digite a quantidade de dados: ')
m(1:n,1:2) = 0
mdados = x_matrix('Dados ', m)
vx = mdados(1:n,1)
vy = mdados(1:n,2)
//Calculando os somatórios
    sx=0
    sx2=0
    sx3=0
    sx4=0
    sxy=0
    sx2y=0
    sy=0
for i=1:n
        sx=sx+vx(i)
        sx2=sx2+vx(i)^2
        sx3=sx3+vx(i)^3
        sx4=sx4+vx(i)^4
        sx2y=sx2y+(vx(i)^2)*vy(i)
        sy=sy+vy(i)
        sxy=sxy+vx(i)*vy(i)
end
//Preenchendo a matriz e vetor do sistema e resolvendo ...
    ma(1,1)=sx2
    ma(1,2)=sx
    ma(1,3)=n
    ma(2,1)=sx3
    ma(2,2)=sx2
    ma(2,3)=sx
    ma(3,1)=sx4
    ma(3,2)=sx3
    ma(3,3)=sx2
    vb(1)=sy
    vb(2)=sxy
    vb(3)=sx2y
    x=inv(ma)*vb
    a=x(1)
    b=x(2)
    c=x(3)
//Calculando o somatório do erro ao quadrado
seq= 0
for i=1:n
        vyc(i)=a*vx(i)^2+b*vx(i)+c
    end
for i=1:n
    seq = seq+(vyc(i)- vy(i))^2
end
erro = seq
//Grafico
clf()
plot2d(vx,vy,-4)
plot2d(vx,vyc,2)
endfunction

//########################################################


//----------------ALGORITMO PRINCIPAL------------------------
//######################################################
 
disp('1- INTERPOLAÇÃO DE LAGRANGE')
disp('2- REGRESSÃO LINEAR')
disp('3- REGRESSÃO EXPONENCIAL y=be^(ax)')
disp('4- REGRESSÃO POTENCIAL y=bx^(a)')
disp('5- REGRESSÃO QUADRÁTICA')  
disp('----------------------------')   
n = input('Escolha a opção: ') 
        if (n==1) then 
            clc        
            disp('Interpolação de Lagrange')
            disp('------------------------------')
            y=lagrange()
            disp(y)                      
        end   
        if (n==2) then 
            clc        
            disp('Regressao Linear y = ax +b')
            disp('-------------------------------')
            [a,b,erro] = reglinear()
            disp(a)
            disp(b)
            disp(erro)                      
        end
        if (n==3) then 
            clc        
            disp('Regressao Exponencial y = Be^(ax)')
            disp('------------------------------')
            [a,b,erro] = rege()
            disp(a)
            disp(b)
            disp(erro)                      
        end   
        if (n==4) then 
            clc        
            disp('Regressao Potencial y = bX^(a)')
            disp('-----------------------------')
            [a,b,erro] = regp()
            disp(a)
            disp(b)
            disp(erro)                      
        end    
        if (n==5) then 
            clc        
            disp('Regressao Quadrática ')
            disp('-----------------------------')
            [a,b, c,erro] = regq()
            disp(a)
            disp(b)
            disp(c)
            disp(erro)                      
        end 
       
disp('Programa Encerrado!') 

