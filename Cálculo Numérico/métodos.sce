clear
clc
//----------------SUB-ROTINAS------------------------
//######################################################
//isolamento de raízes 
function m = isolamento()    
eq=input('Digite a equação: ')
deff('y=f(x)',eq)
dx=input('Digite o deltax: ')
inicio=input('Início da busca: ')
fim=input('fim da busca: ')
linha=0
a=inicio
b=a+dx
while(b<fim)
   ya=f(a)
   yb=f(b)
   if(ya*yb<0) then
     linha=linha+1
     matrizab(linha,1)=a
     matrizab(linha,2)=b   
   end 
   a=a+dx
   b=b+dx
end
m=matrizab
endfunction



//########################################################
//Método da Bissecção
function m = bisseccao()    
eq=input('Digite a equação: ')
deff('y=f(x)',eq)
a=input('Digite o valor de a: ')
b=input('Digite o valor de b: ')
erro = input('Digite o erro: ')
c = (a+ b)/ 2
tabela(1,1) = a
tabela(1,3) = b
tabela(1,2) = c
tabela(1,4) = f(a)
tabela(1,5) = f(c)
tabela(1,6) = f(b)
tabela(1,7) = f(a)*f(c)
i = 1
while(abs(f(c))>erro)
    i= i +1 
    if ((tabela((i-1),7))<0) then
        a = a
        b = c
        c = (a+b)/2
        tabela(i,1) = a
        tabela(i,3) = b
        tabela(i,2) = c
        tabela(i,4) = f(a)
        tabela(i,5) = f(c)
        tabela(i,6) = f(b)
        tabela(i,7) = f(a)*f(c)
    end
    if ((tabela((i-1),7))>=0) then
        a = c
        b = b
        c = (a+b)/2
        tabela(i,1) = a
        tabela(i,3) = b
        tabela(i,2) = c
        tabela(i,4) = f(a)
        tabela(i,5) = f(c)
        tabela(i,6) = f(b)
        tabela(i,7) = f(a)*f(c) 
    end
end
m=tabela

endfunction




//########################################################
//Método da Posição Falsa
function m = falsaposicao()  
eq=input('Digite a equação: ')
deff('y=f(x)',eq)
a=input('Digite o valor de a: ')
b=input('Digite o valor de b: ')
erro = input('Digite o erro: ')
c = (a*f(b) - b*f(a))/(f(b) - f(a))
tabela(1,1) = a
tabela(1,3) = b
tabela(1,2) = c
tabela(1,4) = f(a)
tabela(1,5) = f(c)
tabela(1,6) = f(b)
tabela(1,7) = f(a)*f(c)
i = 1
while((abs(f(c)))>erro)
    i= i +1 
    if ((tabela((i-1),7))<0) then
        a = a
        b = c
        c = (a*f(b) - b*f(a))/(f(b) - f(a))
        tabela(i,1) = a
        tabela(i,3) = b
        tabela(i,2) = c
        tabela(i,4) = f(a)
        tabela(i,5) = f(c)
        tabela(i,6) = f(b)
        tabela(i,7) = f(a)*f(c)
    end
    if ((tabela((i-1),7))>=0) then
        a = c
        b = b
        c = (a*f(b) - b*f(a))/(f(b) - f(a))
        tabela(i,1) = a
        tabela(i,3) = b
        tabela(i,2) = c
        tabela(i,4) = f(a)
        tabela(i,5) = f(c)
        tabela(i,6) = f(b)
        tabela(i,7) = f(a)*f(c) 
    end
end
m=tabela
endfunction







//########################################################
//Método de Newton
function m = newton()  
eq=input('Digite a equação: ')
deff('y=f(x)',eq)
eqd=input('Digite a derivada da equação: ')
deff('y=g(x)',eqd)
x1=input('Digite o valor de x inicial: ')
erro = input('Digite o erro: ')
tabela(1,1) = 1
tabela(1,2) = x1
tabela(1,3) = f(x1)
tabela(1,4) = g(x1)
tabela(1,5) = f(x1) / g(x1)
i=1
while((abs(tabela(i,3)))>erro)
    i= i +1 
    tabela(i,1) = i
    tabela(i,2) = tabela(i-1, 2) - tabela(i-1,5)
    tabela(i,3) = f(tabela(i,2))
    tabela(i,4) = g(tabela(i,2))
    tabela(i,5)= tabela(i,3) / tabela(i,4)
    end
m=tabela
endfunction




//########################################################
//Método da Secante
function m = secante()  
eq=input('Digite a equação: ')
deff('y=f(x)',eq)
x1=input('Digite o valor de x inicial: ')
x2=input('Digite o segundo valor de x inicial: ')
erro = input('Digite o erro: ')
tab(1,1) = 1
tab(1,2) = x1
tab(1,3) = f(x1)
tab(2,1) = 2
tab(2,2) = x2
tab(2,3) = f(x2)
i = 2
  while((abs(tab(i,3)))>erro)
    i= i +1 
    tab(i,1) = i
    aux1 = tab(i-2,2)*tab(i-1,3)
    aux2 = tab(i-1,2)*tab(i-2,3)
    aux3 = tab(i-1,3) - tab(i-2,3)
    tab(i,2) = (aux1 - aux2) / aux3
    tab(i,3) = f(tab(i,2)) 
  end
m=tab
endfunction






//########################################################
//Eliminação de Gauss
function [ma,vb,vx] = gauss()  
//entrada de dados
n=input('Digite N: ')
m(1:n,1:n+1) = 0
mab = x_matrix('Matriz do sistema', m)
//triangularização 
a=mab(1:n,1:n)
b=mab(1:n,n+1)
for j = 1:n-1
    for i =n:-1:j+1
        m= a(i,j)/a(j,j)
        for k=1:n
            a(i,k) = a(i,k) - m*a(j,k)
        end
        b(i) = b(i) - m*b(j)
    end
    
end
//Resolução do Sistema
//Calculo do vetor c
x(n) = b(n)/a(n,n)
for i=n-1:-1:1
    soma=0
    for j=i+1:n
        soma= soma + a(i,j)*x(j)
    end
    x(i) = (b(i)-soma)/a(i,i)
end



ma = a
vb = b
vx = x

endfunction







//----------------ALGORITMO PRINCIPAL------------------------
//######################################################
 
disp('1-ISOLAMENTO')
disp('2-BISSECÇÃO,3-FALSA POSIÇÃO')
disp('4-NEWTON, 5-SECANTE')
disp('6-ELIM. DE GAUSS')  
disp('----------------------------')   
n=input('Escolha a opção: ') 
        if (n==1) then 
            clc        
            disp('Isolamento de Raízes')
            disp('----------------------')
            m=isolamento()
            disp(m)                      
        end     
        if (n==2) then 
            clc        
            disp('Metodo da Bissecção ')
            disp('----------------------')
            m=bisseccao()
            disp(m)                      
        end   
        if (n==3) then 
            clc        
            disp('Método da Falsa Posição ')
            disp('----------------------')
            m=falsaposicao()
            disp(m)                      
        end 
        if (n==4) then 
            clc        
            disp('Método de Newton ')
            disp('----------------------')
            m=newton()
            disp(m)                      
        end   
        if (n==5) then 
            clc        
            disp('Método da Secante ')
            disp('----------------------')
            m=secante()
            disp(m)                      
        end 
        if (n==6) then 
            clc        
            disp('Eliminação de Gauss ')
            disp('----------------------')
            [ma,vb,vx]=gauss()
            disp(ma)
            disp(vb)
            disp(vx)                      
        end   

disp('programa encerrado!') 


