import serial
from struct import unpack
from functools import wraps

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


	# wrappers
	def connectPort( func ):
		@wraps( func )
		def connect( self, *args, **kwargs ):
			self.port.open()
			retVal = func( self, *args, **kwargs )
			self.port.close()
			return retVal
		return connect

	def rememberOption( func ):
		@wraps( func )
		def handleRemember( self, *args, **kwargs ):
			remember = kwargs.pop( 'remember', False )
			if remember:
				# remember on
				self._writeCommand( "0xFE", "0x93", 1 )
			retVal = func( self, *args, **kwargs )
			if remember:
				# remember off
				self._writeCommand( "0xFE", "0x93", 0 )
			return retVal
		return handleRemember


	# display config functions
	@connectPort
	def getDisplaySize( self ):
		self.port.flushInput()
		self._writeCommand( "0xFE", "0xB8" )
		width = self.port.read()
		height = self.port.read()
		self.port.flushInput()
		return unpack( 'B', width )[0], unpack( 'B', height )[0]

	@connectPort
	def displayBacklightOn( self, minutes=0 ):
		self._writeCommand( "0xFE", "0x42", minutes )

	@connectPort
	def displayBacklightOff( self ):
		self._writeCommand( "0xFE", "0x46" )

	@connectPort
	@rememberOption
	def setDisplayColor( self, red, green, blue ):
		self._writeCommand( "0xFE", "0x82", red, green, blue )

	@connectPort
	@rememberOption
	def setDisplayBrightness( self, brightness ):
		self._writeCommand( "0xFE", "0x99", brightness )
	
	@connectPort
	@rememberOption
	def setDisplayContrast( self, contrast ):
		self._writeCommand( "0xFE", "0x50", contrast )


	# keypad config functions
	@connectPort
	def keypadBacklightOff( self, minutes=0 ):
		self._writeCommand( "0xFE", "0x9B", minutes )
	
	@connectPort
	@rememberOption
	def setKeypadBrightness( self, brightness ):
		self._writeCommand( "0xFE", "0x9C", brightness )


	# text and drawing
	@connectPort
	def clearScreen( self ):
		self._writeCommand( "0xFE", "0x58" )

	@connectPort
	def writeString( self, string ):
		self.port.write( string )

	@connectPort
	def setCursorPos( self, column, row ):
		self._writeCommand( "0xFE", "0x47", column, row )

	@connectPort
	def setCursorCord( serf, x, y ):
		self._writeCommand( "0xFE", "0x79", x, y )
	
		

