clear
clc
//----------------SUB-ROTINAS------------------------
//######################################################
//Regra dos trap�zios
function [tab,integral]=trapezio()
//entrada de dados
eq=input('Digite a equa��o: ')
deff('y=f(x)',eq)
a=input('Digite o valor de a: ')   
b=input('Digite o valor de b: ') 
n=input('Digite o n�mero de subdivis�es: ')
h=(b-a)/n;
//coluna 1
for i=1:n
    m(i,1)=i
end
//coluna 2
m(1,2)=a
for i=2:n
    m(i,2)=m(i-1,2)+h
end
//coluna 3
for i=1:n
    m(i,3)=m(i,2)+h
end
//Colunas 4,5 e 6
for i=1:n
    m(i,4)=f(m(i,2))
    m(i,5)=f(m(i,3))
    m(i,6)=(m(i,4)+m(i,5))*(h/2)
end
soma=sum(m(:,6))
tab=m
integral=soma
endfunction



//######################################################
//Regra de simpson
function [tab,integral]=simpson()
//entrada de dados
eq=input('Digite a equa��o: ')
deff('y=f(x)',eq)
a=input('Digite o valor de a: ')   
b=input('Digite o valor de b: ') 
n=input('Digite o n�mero de subdivis�es: ')
h=(b-a)/n;
//coluna 1
for i=1:n
    m(i,1)=i
end
//coluna 2
m(1,2)=a
for i=2:n
    m(i,2)=m(i-1,2)+h
end
//coluna 3
for i=1:n
    m(i,3)=m(i,2)+h
end
//Coluna 4
for i=1:n
    m(i,4)=(m(i,2)+m(i,3))/2
end
//Colunas 5,6,7 e 8
for i=1:n
    m(i,5)=f(m(i,2))
    m(i,6)=f(m(i,3))
    m(i,7)=f(m(i,4))
    m(i,8)=(m(i,5)+4*m(i,7)+m(i,6))*(h/6)
end    
soma=sum(m(:,8))
tab=m
integral=soma
endfunction



//########################################################

//Euler
function [tab,y]=euler()
//entrada de dados
eq=input('Digite a equa��o: ')
deff('dydx=f(x,y)',eq)
xinic=input('Digite o valor do x inicial: ')   
yinic=input('Digite o valor do y inicial: ')    
xdes=input('Digite o valor do x desejado: ')
n=input('Digite o n�mero de itera��es: ')
//processamento
h=(xdes-xinic)/n
m(1,2)=xinic
m(1,3)=yinic
m(1,4)=f(m(1,2),m(1,3))
//preenchimento da coluna 1
for i=1:n+1
    m(i,1)=i    
end
//preenchimento da coluna 2
for i=2:n+1
    m(i,2)=m(i-1,2)+h    
end
//inicio do processo
for i=2:n+1
    m(i,3)=m(i-1,3)+h*m(i-1,4) 
    m(i,4)=f(m(i,2),m(i,3))      
end
//retorno da fun��o
tab=m
y=m(n+1,3)

endfunction
//########################################################



//######################################################
//Kutta
function [tab,y]=kutta()
//entrada de dados
eq=input('Digite a equa��o: ')
deff('dydx=f(x,y)',eq)
xinic=input('Digite o valor do x inicial: ')   
yinic=input('Digite o valor do y inicial: ')    
xdes=input('Digite o valor do x desejado: ')
n=input('Digite o n�mero de itera��es: ')
//processamento
h=(xdes-xinic)/n
m(1,2)=xinic
m(1,7)=yinic
//preenchimento da coluna 1
for i=1:n+1
    m(i,1)=i    
end
//preenchimento da coluna 2
for i=2:n+1
    m(i,2)=m(i-1,2)+h    
end
//inicio do processo
for i=1:n
    xi=m(i,2)
    yi=m(i,7)
    k1=h*f(xi,yi)
    m(i,3)=k1
    k2=h*f(xi+h/2,yi+k1/2)
    m(i,4)=k2
    k3=h*f(xi+h/2,yi+k2/2)
    m(i,5)=k3
    k4=h*f(xi+h,yi+k3)
    m(i,6)=k4
    m(i+1,7)=yi+k1/6+k2/3+k3/3+k4/6
      
end
//retorno da fun��o
tab=m
y=m(i+1,7)

endfunction

//########################################################

//########################################################


//----------------ALGORITMO PRINCIPAL------------------------
//######################################################
 
disp('1- INTEGRAL - REGRA DOS TRAP�ZIOS')
disp('2- INTEGRAL - REGRA DE SIMPSON')
disp('3- EQUA��O DIFERENCIAL - EULER')
disp('4- EQUA��O DIFERENCIAL - RUNGE-KUTTA')  
disp('----------------------------')   
n = input('Escolha a op��o: ') 
        if (n==1) then 
            clc        
            disp('INTEGRAL - REGRA DOS TRAP�ZIOS')
            disp('------------------------------')
            [tab,integral]=trapezio()
            disp('tabela')
            disp(tab)
            disp('resultado')
            disp(integral)                      
        end   
        if (n==2) then 
            clc        
            disp('INTEGRAL - REGRA DE SIMPSON')
            disp('------------------------------')
            [tab,integral]=simpson()
            disp('tabela')
            disp(tab)
            disp('resultado')
            disp(integral)          
        end
        if (n==3) then 
            clc        
            disp('EDO - Euler')
            [tab,y]=euler()
            disp('tabela')
            disp(tab)
            disp('y desejado')
            disp(y)
                                
        end   
        if (n==4) then 
            clc        
            disp('EDO - Runge Kutta')
            disp('-----------------------------')
            [tab,y] = kutta()
            disp('tabela')
            disp(tab)
            disp('y desejado')
            disp(y)                      
        end    
 
       
disp('Programa Encerrado!') 
