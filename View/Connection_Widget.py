#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from PyQt5 import QtGui, QtWidgets, QtCore

# TODO: Change
import pydotplus as Pydot

from camkes.ast import *

from Model import Common
from Instance_Widget import InstanceWidget


# TODO: Make connectionWidget totally independent of connection_object. Have links to the nodes that its connecting.
class ConnectionWidget(QtWidgets.QGraphicsItem):

    @property
    def connection_object(self):
        return self._connection_object

    @connection_object.setter
    def connection_object(self, value):
        assert isinstance(value, Connection)
        self._connection_object = value

    @property
    def edge(self):
        return self._edge

    @edge.setter
    def edge(self, value):
        assert isinstance(value, Pydot.Edge)
        self._edge = value

    @property
    def edge_points(self):
        return self._edge_points

    @edge_points.setter
    def edge_points(self, value):
        assert isinstance(value, list)
        # TODO: Change from edge point to tuple
        # TODO: Different method
        if len(value) >= 2:
            assert isinstance(value[1], tuple)
            self.path.moveTo(value[1][0], value[1][1])

        if len(value) >= 3:
            for point in value[2:]:
                self.path.lineTo(point[0], point[1])

        assert isinstance(value[0], tuple)
        self.path.lineTo(value[0][0], value[0][1])

        # assert isinstance(value[-1], tuple)
        # self.path.lineTo(value[-1][0], value[-1][1])

        self._edge_points = value

        self.prepareGeometryChange()

    @property
    def path(self):
        # Lazy Instantiation
        if self._path is None:
            self._path = QtGui.QPainterPath()
        return self._path

    def clear_path(self):
        self._path = None

    @property
    def source_instance_widget(self):
        return self._source_instance_widget

    @source_instance_widget.setter
    def source_instance_widget(self, value):
        assert isinstance(value, InstanceWidget)
        self._source_instance_widget = value

    @property
    def dest_instance_widget(self):
        return self._dest_instance_widget

    @dest_instance_widget.setter
    def dest_instance_widget(self, value):
        assert isinstance(value, InstanceWidget)
        self._dest_instance_widget = value

    def __init__(self, connection_object, source, dest, edge=None):
        super(ConnectionWidget, self).__init__()
        assert isinstance(connection_object, Connection)
        self._connection_object = connection_object
        self._edge = edge
        self._edge_points = None
        self._path = None

        assert isinstance(source, InstanceWidget)
        self._source_instance_widget = source

        assert isinstance(dest, InstanceWidget)
        self._dest_instance_widget = dest

        # Get points from attributes of the edge
        if edge:
            edge_attributes = edge.get_attributes()
            edge_points = Common.extract_numbers(edge_attributes['pos'])
            self.edge_points = edge_points

    def paint(self, q_painter, style_option , widget=None):

        # assert isinstance(style_option, QtWidgets.QStyleOptionGraphicsItem)
        # assert isinstance(widget, QtWidgets.QWidget)

        assert isinstance(q_painter, QtGui.QPainter)

        # stroker = QtGui.QPainterPathStroker()
        # stroker.setWidth(5)
        # self.path.addPath(stroker.createStroke(self.path))

        q_painter.drawPath(self.path)

    def boundingRect(self):
        rect = self.path.boundingRect()
        assert isinstance(rect, QtCore.QRectF)
        rect.adjust(-2.5,-2.5,2.5,2.5)

        return rect

    def shape(self):
        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(5)
        return stroker.createStroke(self.path)

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        print self.connection_object.name + " clicked (edge)"
        
    # Method using QPainter to draw the edge points, spline
    # def draw_connection(self, q_painter):
    #     assert isinstance(q_painter, QtGui.QPainter)
    #     q_painter.drawPath(self.path)
    #
    #     '''
    #     color = QtGui.QColor(0,0,0)
    #     pen = q_painter.pen()
    #     pen.setColor(color)
    #     q_painter.setPen(pen)
    #
    #     for point in self.edge_points:
    #
    #         color = q_painter.pen().color()
    #         print "Before: " + str(color.red()) + " " + str(color.green()) + " " + str(color.blue())
    #         color.setRed(color.red()+30)
    #         print str(color.red()) + " " + str(color.green()) + " " + str(color.blue())
    #
    #         pen = q_painter.pen()
    #         pen.setColor(color)
    #         q_painter.setPen(pen)
    #
    #         color = q_painter.pen().color()
    #         print "after" + str(color.red()) + " " + str(color.green()) + " " + str(color.blue())
    #
    #         q_painter.drawPoint(point[0], point[1])
    #         q_painter.fillRect(QtCore.QRect(point[0], point[1], 4,4), color)
    #     '''
