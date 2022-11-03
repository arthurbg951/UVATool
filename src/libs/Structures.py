from Drawing import(
    NodeDraw, ElementDraw, Support, Apoio, NodalForce, Rectangle
)


class Structures:
    @staticmethod
    def balanco() -> tuple[list[NodeDraw], list[ElementDraw]]:
        n1 = NodeDraw(0, 0)
        n2 = NodeDraw(100, 0)
        n1.setSupport(Support.fixed)
        n2.setNodalForce(NodalForce(0, 10, 0))
        e1 = ElementDraw(n1, n2, 1, 1, 1)
        nodes = [n1, n2]
        elements = [e1]

        return nodes, elements

    @staticmethod
    def edificio3Andares() -> tuple[list[NodeDraw], list[ElementDraw]]:
        secao = Rectangle(0.12, 0.01)
        area = secao.area
        inercia = secao.inertia
        young = 200e9
        n1 = NodeDraw(0, -0)
        n2 = NodeDraw(150, -0)
        n3 = NodeDraw(0, -30)
        n4 = NodeDraw(150, -30)
        n5 = NodeDraw(0, -60)
        n6 = NodeDraw(150, -60)
        n7 = NodeDraw(0, -90)
        n8 = NodeDraw(150, -90)
        print(n2.x, n2.y, n2.getItem().x(), n2.getItem().y())
        n1.setSupport(Apoio.segundo_genero)
        n2.setSupport(Apoio.primeiro_genero)
        n3.setNodalForce(NodalForce(-100, 0, 0))
        n5.setNodalForce(NodalForce(-100, 0, 0))
        n7.setNodalForce(NodalForce(-100, 0, 0))
        e1 = ElementDraw(n1, n3, area, inercia, young)
        e2 = ElementDraw(n2, n4, area, inercia, young)
        e3 = ElementDraw(n3, n4, area, inercia, young)
        e4 = ElementDraw(n3, n5, area, inercia, young)
        e5 = ElementDraw(n4, n6, area, inercia, young)
        e6 = ElementDraw(n5, n6, area, inercia, young)
        e7 = ElementDraw(n5, n7, area, inercia, young)
        e8 = ElementDraw(n6, n8, area, inercia, young)
        e9 = ElementDraw(n7, n8, area, inercia, young)
        nodes = [n1, n2, n3, n4, n5, n6, n7, n8]
        elements = [e1, e2, e3, e4, e5, e6, e7, e8, e9]

        return nodes, elements

    @staticmethod
    def porticosSucessivos() -> tuple[list[NodeDraw], list[ElementDraw]]:
        nodes = []
        elements = []

        rec = Rectangle(0.012, 0.001)
        area = rec.area
        inercia = rec.inertia

        n1 = NodeDraw(0, 0)
        n1.setSupport(Apoio.terceiro_genero)
        n2 = NodeDraw(0, 10)
        n3 = NodeDraw(10, 10)
        n4 = NodeDraw(10, 0)
        n4.setSupport(Apoio.terceiro_genero)

        e1 = ElementDraw(n1, n2, area, inercia, 1)
        e2 = ElementDraw(n2, n3, area, inercia, 1)
        e3 = ElementDraw(n3, n4, area, inercia, 1)

        nodes.append(n1)
        nodes.append(n2)
        nodes.append(n3)
        nodes.append(n4)

        elements.append(e1)
        elements.append(e2)
        elements.append(e3)

        for i in range(2, 100, 1):
            n2, n3 = NodeDraw(0, -i*10), NodeDraw(1*10, -i*10)

            e1 = ElementDraw(nodes[len(nodes)-4], n2, area, inercia, 1)
            e2 = ElementDraw(n2, n3, area, inercia, 1)
            e3 = ElementDraw(n3, nodes[len(nodes)-1], area, inercia, 1)

            nodes.append(n2)
            nodes.append(n3)
            elements.append(e1)
            elements.append(e2)
            elements.append(e3)

        nodes[len(nodes)-2].setNodalForce(NodalForce(100, 0, 0))

        return nodes, elements

    @staticmethod
    def modelotcc() -> tuple[list[NodeDraw], list[ElementDraw]]:

        secao = Rectangle(0.20, 0.40)
        area = secao.area
        inercia = secao.inertia
        young = 25e9

        n1 = NodeDraw(0, -0)
        n2 = NodeDraw(400, -0)
        n3 = NodeDraw(0, -150)
        n4 = NodeDraw(100, -150)
        n5 = NodeDraw(300, -150)
        n6 = NodeDraw(400, -150)
        n7 = NodeDraw(0, -300)
        n8 = NodeDraw(400, -300)

        n1.setSupport(Apoio.terceiro_genero)
        n2.setSupport(Apoio.terceiro_genero)
        n7.setSupport(Apoio.terceiro_genero)
        n8.setSupport(Apoio.terceiro_genero)

        n3.setP(1)
        n3.setSupport(Apoio.rotula)
        n6.setP(1)

        n4.setNodalForce(NodalForce(100e3, -100e3, 0))
        n5.setNodalForce(NodalForce(-100e3, 0, 0))

        e1 = ElementDraw(n1, n3, area, inercia, young)
        e2 = ElementDraw(n3, n4, area, inercia, young)
        e3 = ElementDraw(n4, n5, area, inercia, young)
        e4 = ElementDraw(n5, n6, area, inercia, young)
        e5 = ElementDraw(n2, n6, area, inercia, young)
        e6 = ElementDraw(n3, n7, area, inercia, young)
        e7 = ElementDraw(n6, n8, area, inercia, young)

        nodes = [n1, n2, n3, n4, n5, n6, n7, n8]
        elements = [e1, e2, e3, e4, e5, e6, e7]

        return nodes, elements

    @staticmethod
    def momentorotacaoVigaBalanco() -> tuple[list[NodeDraw], list[ElementDraw]]:
        # Materiais ----------------------------------------------------------------------------------
        secao_p = Rectangle(0.2 * 10, 0.2 * 10)  # hy x hx
        area_p = secao_p.area
        inercia_p = secao_p.inertia
        secao_v = Rectangle(0.15 * 10, 0.6 * 10)  # base x altura
        area_v = secao_v.area
        inercia_v = secao_v.inertia
        young = 27e9 / 10e3

        # Nós ----------------------------------------------------------------------------------------
        n1 = NodeDraw(0, -0)
        n2 = NodeDraw(0, -3 * 10)
        n3 = NodeDraw(2 * 10, -3 * 10)

        # Apoios -------------------------------------------------------------------------------------
        n1.setSupport(Apoio.terceiro_genero)

        # Fator Pi -----------------------------------------------------------------------------------
        n2.setP(1)

        # Cargas -------------------------------------------------------------------------------------
        n3.setNodalForce(NodalForce(0, -10e3, 0))

        # --------------------------------------------------------------------------------------------
        e1 = ElementDraw(n1, n2, area_p, inercia_p, young)
        e2 = ElementDraw(n2, n3, area_v, inercia_v, young)

        nodes = [n1, n2, n3]
        elements = [e1, e2]

        return nodes, elements

    @staticmethod
    def momentorotacaoPortico() -> tuple[list[NodeDraw], list[ElementDraw]]:
        # Materiais ----------------------------------------------------------------------------------
        secao_p = Rectangle(0.2 * 10, 0.2 * 10)  # hy x hx
        area_p = secao_p.area
        inercia_p = secao_p.inertia
        secao_v = Rectangle(0.15 * 10, 0.6 * 10)  # base x altura
        area_v = secao_v.area
        inercia_v = secao_v.inertia
        young = 27e9 / 10e3

        # Nós ----------------------------------------------------------------------------------------
        n1 = NodeDraw(0 * 10, -0 * 10)
        n2 = NodeDraw(0 * 10, -3 * 10)
        n3 = NodeDraw(2 * 10, -3 * 10)
        n4 = NodeDraw(4 * 10, -3 * 10)
        n5 = NodeDraw(6 * 10, -3 * 10)
        n6 = NodeDraw(6 * 10, -0 * 10)

        # Apoios -------------------------------------------------------------------------------------
        n1.setSupport(Apoio.terceiro_genero)
        n6.setSupport(Apoio.terceiro_genero)

        # Fator Pi -----------------------------------------------------------------------------------
        n2.setP(1)
        n5.setP(1)

        # Cargas -------------------------------------------------------------------------------------
        n3.setNodalForce(NodalForce(0, -10e3, 0))
        n4.setNodalForce(NodalForce(0, -10e3, 0))

        # --------------------------------------------------------------------------------------------
        e1 = ElementDraw(n1, n2, area_p, inercia_p, young)
        e2 = ElementDraw(n2, n3, area_v, inercia_v, young)
        e3 = ElementDraw(n3, n4, area_v, inercia_v, young)
        e4 = ElementDraw(n4, n5, area_v, inercia_v, young)
        e5 = ElementDraw(n5, n6, area_p, inercia_p, young)

        nodes = [n1, n2, n3, n4, n5, n6]
        elements = [e1, e2, e3, e4, e5]

        return nodes, elements

    @staticmethod
    def modeloBielasETirantes() -> tuple[list[NodeDraw], list[ElementDraw]]:
        # Materiais ----------------------------------------------------------------------------------
        secao_p = Rectangle(1, 1)  # hy x hx
        area_p = secao_p.area
        inercia_p = secao_p.inertia
        secao_v = Rectangle(1, 1)  # base x altura
        area_v = secao_v.area
        inercia_v = secao_v.inertia
        young = 1

        # Nós ----------------------------------------------------------------------------------------
        n1 = NodeDraw(0 * 10, -0 * 10)
        n2 = NodeDraw(10 * 10, -0 * 10)
        n3 = NodeDraw(20 * 10, -0 * 10)
        n4 = NodeDraw(30 * 10, -0 * 10)
        n5 = NodeDraw(60 * 10, -0 * 10)
        n6 = NodeDraw(70 * 10, -0 * 10)
        n7 = NodeDraw(80 * 10, -0 * 10)
        n8 = NodeDraw(90 * 10, -0 * 10)

        n9 = NodeDraw(10 * 10, -11.7 * 10)
        n10 = NodeDraw(20 * 10, -11.7 * 10)
        n11 = NodeDraw(30 * 10, -11.7 * 10)
        n12 = NodeDraw(60 * 10, -11.7 * 10)
        n13 = NodeDraw(70 * 10, -11.7 * 10)
        n14 = NodeDraw(80 * 10, -11.7 * 10)

        # Apoios -------------------------------------------------------------------------------------
        n1.setSupport(Apoio.segundo_genero)
        n8.setSupport(Apoio.primeiro_genero)

        # Fator Pi -----------------------------------------------------------------------------------
        # n2.setP(1e-32)
        # n3.setP(1e-32)
        # n4.setP(1e-32)
        # n5.setP(1e-32)
        # n6.setP(1e-32)
        # n7.setP(1e-32)

        # n9.setP(1e-32)
        # n10.setP(1e-32)
        # n11.setP(1e-32)
        # n12.setP(1e-32)
        # n13.setP(1e-32)
        # n14.setP(1e-32)

        # Cargas -------------------------------------------------------------------------------------
        n11.setNodalForce(NodalForce(0, -10e3, 0))
        n12.setNodalForce(NodalForce(0, -10e3, 0))

        # --------------------------------------------------------------------------------------------
        e1 = ElementDraw(n1, n2, area_p, inercia_p, young)
        e2 = ElementDraw(n2, n3, area_v, inercia_v, young)
        e3 = ElementDraw(n3, n4, area_v, inercia_v, young)
        e4 = ElementDraw(n4, n5, area_v, inercia_v, young)
        e5 = ElementDraw(n5, n6, area_p, inercia_p, young)
        e6 = ElementDraw(n6, n7, area_p, inercia_p, young)
        e7 = ElementDraw(n7, n8, area_p, inercia_p, young)

        e8 = ElementDraw(n9, n10, area_p, inercia_p, young)
        e9 = ElementDraw(n10, n11, area_p, inercia_p, young)
        e10 = ElementDraw(n11, n12, area_p, inercia_p, young)
        e11 = ElementDraw(n12, n13, area_p, inercia_p, young)
        e12 = ElementDraw(n13, n14, area_p, inercia_p, young)

        e13 = ElementDraw(n1, n9, area_p, inercia_p, young)
        e14 = ElementDraw(n2, n10, area_p, inercia_p, young)
        e15 = ElementDraw(n3, n11, area_p, inercia_p, young)
        e16 = ElementDraw(n6, n12, area_p, inercia_p, young)
        e17 = ElementDraw(n7, n13, area_p, inercia_p, young)
        e18 = ElementDraw(n8, n14, area_p, inercia_p, young)

        e19 = ElementDraw(n2, n9, area_p, inercia_p, young)
        e20 = ElementDraw(n3, n10, area_p, inercia_p, young)
        e21 = ElementDraw(n4, n11, area_p, inercia_p, young)
        e22 = ElementDraw(n5, n12, area_p, inercia_p, young)
        e23 = ElementDraw(n6, n13, area_p, inercia_p, young)
        e24 = ElementDraw(n7, n14, area_p, inercia_p, young)

        nodes = [n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14]
        elements = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18,
                    e19, e20, e21, e22, e23, e24]

        return nodes, elements

    @staticmethod
    def porticoSimples() -> tuple[list[NodeDraw], list[ElementDraw]]:
        # ESTRUTURA EXEMPLO APRESENTADA NA IC UVA 2022.2
        # Seções --------------------------------------------------------------------------------------
        secao_p = Rectangle(0.2, 0.6)  # hy x hx
        area_p = secao_p.area
        inercia_p = secao_p.inertia
        secao_v = Rectangle(0.15, 0.6)  # base x altura
        area_v = secao_v.area
        inercia_v = secao_v.inertia
        # Materiais -----------------------------------------------------------------------------------
        young = 27_000_000_000
        # Nos -----------------------------------------------------------------------------------------
        n1 = NodeDraw(0, 0)
        n2 = NodeDraw(0, -30)
        n3 = NodeDraw(30, -30)
        n4 = NodeDraw(50, -30)
        n5 = NodeDraw(80, -30)
        n6 = NodeDraw(80, 0)
        # Elementos -----------------------------------------------------------------------------------
        e1 = ElementDraw(n1, n2, area_p, inercia_p, young)
        e2 = ElementDraw(n2, n3, area_v, inercia_v, young)
        e3 = ElementDraw(n3, n4, area_v, inercia_v, young)
        e4 = ElementDraw(n4, n5, area_v, inercia_v, young)
        e5 = ElementDraw(n5, n6, area_p, inercia_p, young)
        # Apoios --------------------------------------------------------------------------------------
        n1.setSupport(Apoio.terceiro_genero)
        n6.setSupport(Apoio.terceiro_genero)
        # Forças --------------------------------------------------------------------------------------
        n3.setNodalForce(NodalForce(0, -10_000, 0))
        n4.setNodalForce(NodalForce(0, -10_000, 0))

        nodes = [n1, n2, n3, n4, n5, n6]
        elements = [e1, e2, e3, e4, e5]

        return nodes, elements
