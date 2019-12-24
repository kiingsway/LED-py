#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#	Fazer parar o Lightpainting (lightpaint.py) quando um botão for pressionado (swayledNOVO.py)
#	Armazena se o lightpaint deve se manter ligado ou desligado
lpLigado = False
#	Armazena a imagem (swayled.py) para o lightpainting (lightpaint.py)
imagem_arquivo = ''
#	Armazena a entrada de velocidade (swayled.py) para o lightpainting (lightpaint.py)
taxa_coluna = 1
taxa_frame = 100

reverter_x = False
reverter_y = False

outroEfeitoRainbow = False

outrosEfeitos_old = None