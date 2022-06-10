from libs.UVATool import *

n1 = Node(0, 0)
n2 = Node(1, 1)

e1 = Element(n1, n2, 1, 1, 1)
e2 = Element(n2, n1, 1, 1, 1)

primeiroQuadrante = e1.getAngle() * 180/math.pi
terceiroQuadrante = e2.getAngle() * 180/math.pi

n1 = Node(0, 0)
n2 = Node(1, -1)

e1 = Element(n1, n2, 1, 1, 1)
e2 = Element(n2, n1, 1, 1, 1)
quartoQuadrante = e1.getAngle() * 180/math.pi
segundoQuadrante = e2.getAngle() * 180/math.pi

print("primeiro quadrante ", primeiroQuadrante)
print("segundo quadrante ", segundoQuadrante)
print("terceiro quadrante ", terceiroQuadrante)
print("quarto quadrante ", quartoQuadrante)

n1 = Node(0, 0)
n2 = Node(0, 1)

e1 = Element(n1, n2, 1, 1, 1)
e2 = Element(n2, n1, 1, 1, 1)
print(e1.getAngle() * 180/math.pi)
print(e2.getAngle() * 180/math.pi)
