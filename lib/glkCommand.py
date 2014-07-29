import serial
from struct import unpack

class connection:
	def __init__( self, com, baud_rate=19200 ):
		self.port = serial.Serial( com - 1, baud_rate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, timeout=.1 )
		self.port.close()
		self.width, self.height = self.getDisplaySize()

	def _writeCommand( self, *args ):
		for arg in args:
			if isinstance( arg, basestring ) and arg.startswith( "0x" ):
				self.port.write( arg[2:].decode('hex') )
			elif isinstance( arg, basestring ):
				self.port.write( arg )
			else:
				self.port.write( chr(arg) )

	def _rememberOn( self ):
		self._writeCommand( "0xFE", "0x93", 1 )

	def _rememberOff( self ):
		self._writeCommand( "0xFE", "0x93", 0 )

	
	# display config functions
	def getDisplaySize( self ):
		self.port.open()
		self.port.flushInput()
		self._writeCommand( "0xFE", "0xB8" )
		width = self.port.read()
		height = self.port.read()
		self.port.flushInput()
		self.port.close()
		return unpack( 'B', width )[0], unpack( 'B', height )[0]

	def displayBacklightOn( self, minutes=0 ):
		self.port.open()
		self._writeCommand( "0xFE", "0x42", minutes )
		self.port.close()

	def displayBacklightOff( self ):
		self.port.open()
		self._writeCommand( "0xFE", "0x46" )
		self.port.close()

	def setDisplayColor( self, red, green, blue, remember=0 ):
		self.port.open()
		if remember:
			self._rememberOn()
		self._writeCommand( "0xFE", "0x82", red, green, blue )
		if remember:
			self._rememberOff()
		self.port.close()

	def setDisplayBrightness( self, brightness, remember=0 ):
		self.port.open()
		if remember:
			self._rememberOn()
		self._writeCommand( "0xFE", "0x99", brightness )
		if remember:
			self._rememberOff()
		self.port.close()
	
	def setDisplayContrast( self, contrast, remember=0 ):
		self.port.open()
		if remember:
			self._rememberOn()
		self._writeCommand( "0xFE", "0x50", contrast )
		if remember:
			self._rememberOff()
		self.port.close()
	
	# keypad config functions
	def keypadBacklightOff( self, minutes=0 ):
		self.port.open()
		self._writeCommand( "0xFE", "0x9B" )
		self.port.close()
	
	def setKeypadBrightness( self, brightness, remember=0 ):
		self.port.open()
		if remember:
			self._rememberOn()
		self._writeCommand( "0xFE", "0x9C", brightness )
		if remember:
			self._rememberOff()
		self.port.close()

	# text and drawing
	def clearScreen( self ):
		self.port.open()
		self._writeCommand( "0xFE", "0x58" )
		self.port.close()

	def writeString( self, string ):
		self.port.open()
		self.port.write( string )
		self.port.close()

	def setCursorPos( self, column, row ):
		self.port.open()
		self._writeCommand( "0xFE", "0x47", column, row )
		self.port.close()

	def setCursorCord( serf, x, y ):
		self.port.open()
		self._writeCommand( "0xFE", "0x79", x, y )
		self.port.close()
	
		

