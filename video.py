#
#
#  Copyright 2017 OKAN ACAR <acarokan55@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

#! usr/bin/env python
#! -*- coding:utf-8 -*-

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.properties import BooleanProperty,ObjectProperty
from kivy.uix.label import Label
from kivy.config import Config

import pysrt




	
	
class video_alan(RelativeLayout):
	
	fullscreen = BooleanProperty(False)
	f = ObjectProperty()
	Config.set('kivy', 'exit_on_escape', '0')
	
	def __init__(self,**kwargs):
		
		Window.bind(on_dropfile=self.calistir)
		Window.bind(mouse_pos = self.on_motion)
		
		super(video_alan,self).__init__(**kwargs)
		
		self.video.bind(position = self.slider)
		
		self.keyboard = Window.request_keyboard(self.keyboard_closed,self,"text")
		
		self.keyboard.bind(on_key_down = self.on_keyboard_down)
		
		self.keyboard.bind(on_key_up = self.on_keyboard_up)
	
	def keyboard_closed(self):
		
		self.keyboard.unbind(on_key_down = self.on_keyboard_down)
		
		self.keyboard = None
	
	def on_keyboard_down(self,keyboard,keycode,text,modifiers):
		
		
		
		if self.video.loaded:
			
			if keycode[1] == "right":
				
				self.video.unbind(position = self.slider)
				
				self.video.seek(float(self.video.position)/float(self.video.duration) + 5.0/self.video.duration)
			
			elif keycode[1] == "left":
				
				self.video.unbind(position = self.slider)
				self.video.seek(float(self.video.position)/float(self.video.duration) - 5.0/self.video.duration)
				
				if float(self.video.position)/float(self.video.duration) < 5.0/self.video.duration:
					
					self.video.seek(0)
					
			
			elif keycode[1] == "spacebar":
				
				if self.video.state == "play":
					
					self.video.state = "pause"
				
				elif self.video.state == "pause" or  self.video.state == "stop":
					
					self.video.state = "play"
			
			elif keycode[1] == "enter":
				
				if self.fullscreen:
					
					self.video.pos_hint = {"x":0,"y":0.1}
					Window.fullscreen = False
					self.durumcubugu.pos_hint = {"x":0,"y":0}
					self.fullscreen = not self.fullscreen 
				
				else:
					self.video.pos_hint = {"x":0,"y":0}
					Window.fullscreen = True
					self.size_hint = (1,1)
					Window.size = (1366,768)
					self.durumcubugu.pos_hint = {"x":0,"top":0}
					self.fullscreen = not self.fullscreen
			
			elif keycode[1] == "escape":
				
				if self.fullscreen:
					
					self.video.pos_hint = {"x":0,"y":0.1}
					Window.fullscreen = False
					self.durumcubugu.pos_hint = {"x":0,"y":0}
					self.fullscreen = not self.fullscreen 
				
				else:
					pass
		
		else:
			pass
		
	
	
	def on_keyboard_up(self,keyboard,keycode):
		
		self.video.bind(position = self.slider)
		
		
			
		
		
		
	
	
	def slider(self,ins,val):
		
		if self.video.loaded:	
			m , s = divmod(self.video.position,60)
			h , m = divmod(m,60)
			
			self.zaman = str(int(h)) + ":" + str(int(m)) + ":" + str(int(s))
			
			self.ilerleme.value = float(val)/ float(ins.duration)
			
			if self.f:
				
				if self.zaman in self.sub_list.keys():
					self.altyazi.text = self.sub_list[self.zaman]
				
				if self.zaman in self.sub_list_e:
					self.altyazi.text = ""
		else:
			pass
	
	def oynat(self):
		if self.video.loaded:
			self.video.state = "play"
		else:
			pass
	
	def duraklat(self):
		
		if self.video.loaded:
			self.video.state = "pause"
		else:
			pass

	def durdur(self):
		
		if self.video.loaded:
			self.video.state = "stop"
			self.ilerleme.value = 0,0
		else:
			pass
		
	
	def calistir(self,window,path):
		self.sub_list = {}
		self.sub_list_e = []
		self.giris.opacity = 0
		self.altyazi.text = ""
		
		if path.decode("utf-8").endswith(".srt"):
			
			self.f = pysrt.open(path,encoding='iso-8859-9')
			
			for i in self.f:
				self.sub_list[str(i.start.hours) + ":" + str(i.start.minutes) +":" + str(i.start.seconds)] = "[b]" + (i.text.replace("<","[")).replace(">","]") + "[/b]"
			
			for i in self.f:	 
				
				if str(i.end.hours) + ":" + str(i.end.minutes) +":" + str(i.end.seconds) not in self.sub_list:
					
					self.sub_list_e.append(str(i.end.hours) + ":" + str(i.end.minutes) +":" + str(i.end.seconds))

			
		else:
			self.video.source = path.decode("utf-8")
		
				
	def on_touch_down(self,touch):
		if self.video.loaded:
			if "button" in touch.profile:
				
				
				if touch.button == "scrolldown":
					
					self.video.volume += 0.05
					
					if self.video.volume > 2:
						
						self.video.volume = 2
				
				if touch.button == "scrollup":
					
					self.video.volume -= 0.05
					
					if self.video.volume < 0:
						
						self.video.volume = 0
						
						
			
			if self.video.collide_point(*touch.pos):
				if touch.is_double_tap:
						
					
					if self.fullscreen:
						self.video.pos_hint = {"x":0,"y":0.1}
						Window.fullscreen = False
						self.durumcubugu.pos_hint = {"x":0,"y":0}
						Config.set('graphics', 'show_cursor', "1")
						self.fullscreen = not self.fullscreen 
					
					else:
						
						self.video.pos_hint = {"x":0,"y":0}
						Window.fullscreen = True
						self.size_hint = (1,1)
						Window.size = (1366,768)
						self.durumcubugu.pos_hint = {"x":0,"top":0}
						Config.set('graphics', 'show_cursor', "0")
						self.fullscreen = not self.fullscreen
						
					
					
						
				
			
			if self.ilerleme.collide_point(*touch.pos):
				
				self.video.unbind(position = self.slider)

			
			super(video_alan,self).on_touch_down(touch)
		
		else:
			pass
	
	def on_touch_up(self,touch):
		
		if self.video.loaded:
			
			if self.ilerleme.collide_point(*touch.pos):
				
			
				self.video.seek(self.ilerleme.value)
			
				self.video.bind(position = self.slider)
			
			super(video_alan,self).on_touch_up(touch)
		
		else:
			pass
	
	def on_motion(self,text,pos):
		
		if self.video.loaded:
			
			if self.fullscreen:
			
				if pos[1] < 77:
					self.durumcubugu.pos_hint = {"x":0,"y":0}
				else:
					self.durumcubugu.pos_hint = {"x":0,"top":0}
		
		else:
			pass
				
				
				
			
		

class video(App):
	
	def build(self):
		
		return video_alan()
		

if __name__ == "__main__":
	Window.clearcolor = (0,0,0,0)
	video().run()
