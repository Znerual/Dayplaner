from tkinter import *


class Farbkonzept():
    @staticmethod
    def vormittag():
        return '#ffdc73'

    @staticmethod
    def vormittag_markiert():
        return '#ffbf00'

    @staticmethod
    def mittagspause():
        return '#ffc57f'

    @staticmethod
    def mittagspause_markiert():
        return '#ff8c00'

    @staticmethod
    def nachmittag():
        return '#c0ebe7'

    @staticmethod
    def nachmittag_markiert():
        return '#81d8d0'

    # Linien
    @staticmethod
    def Linien(element):
        color = '#a7adba'
        element.configure(bg=color)
        return color

    @staticmethod
    def Linien_markiert(element):
        color = '#5d5d5d'
        element.configure(bg=color)
        return color

