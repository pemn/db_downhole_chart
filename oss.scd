* Maptek, Australia
* ENVISAGE COLOUR SCHEMES
* Filename : <PROJ>.SCD
*  
*  
* COLOUR TABLE
*      Colour, Red, Blue, Green
*  
* BLOCK, Block Model colour schemes,
*      Colour, From, To
* CHANNEL, Channel colour schemes,
*  ALPHA or NUMERIC
*  Numeric: Colour, From, To,
*  Alpha:   Colour, Character Match,
* CONTOUR, map file and grid drape colour schemes
*      Colour, From, To, Interval
* DRILL, Geology colour schemes,
*  Field Name @ implies character
*  Optionally #RECORD,FROM,TO,THICK,COLOUR
*  Numeric: Colour, From, To,
*  Alpha:   Colour, Character Match,
* GEOTECH, Geotech colour schemes,
*  Field Name @ implies character
*  Numeric: Colour, From, To,
*  Alpha:   Colour, Character Match,
* MAP, Map colour schemes,
*      Colour, From, To
* MISTIE, Mistie colour schemes,
*      Colour, From, To
* SAMPLES, Samples colour schemes,
*  ALPHA or NUMERIC
*  Numeric: Colour, From, To,
*  Alpha:   Colour, Character Match,
* SEISMIC, Seismic colour schemes,
*      Colour, Horizon Value
* STRATA, Strata colour schemes,
*      Colour, Value
* TEXTURE, Texture colour schemes,
*      Colour, From, To
* PATTERN, Pattern colour schemes,
*  ALPHA or range mode
*   GELT : Start <= Val <  End
*   GTLE : Start <  Val <= End
*   GELE : Start <= Val <= End
*   Numeric: Colour, Pattern, From, To,
*   Alpha:   Colour, Pattern, Character Match,
*
*  Written: 06-Jul-2012 08:12:07*
*
*
*
*
*
*
*
BEGIN$DEF DEVICE_COLOUR
	BEGIN$TAB GEO
		'1'
		'15'
		'15'
		'15'
		'2'
		'14'
		'0'
		'0'
		'3'
		'14'
		'13'
		'0'
		'4'
		'14'
		'12'
		'12'
		'5'
		'12'
		'8'
		'8'
		'6'
		'0'
		'8'
		'4'
		'7'
		'0'
		'15'
		'8'
		'8'
		'0'
		'15'
		'12'
		'9'
		'0'
		'13'
		'0'
		'10'
		'6'
		'9'
		'0'
		'11'
		'7'
		'13'
		'6'
		'12'
		'15'
		'11'
		'14'
		'13'
		'7'
		'0'
		'4'
		'14'
		'13'
		'7'
		'12'
		'15'
		'7'
		'5'
		'6'
		'16'
		'14'
		'10'
		'13'
		'17'
		'12'
		'0'
		'8'
		'18'
		'0'
		'0'
		'10'
		'19'
		'3'
		'1'
		'6'
		'20'
		'9'
		'7'
		'5'
		'21'
		'12'
		'9'
		'11'
		'22'
		'0'
		'11'
		'11'
		'23'
		'15'
		'13'
		'9'
		'24'
		'15'
		'0'
		'15'
		'25'
		'9'
		'9'
		'11'
		'26'
		'7'
		'11'
		'15'
		'27'
		'7'
		'15'
		'10'
		'28'
		'15'
		'8'
		'7'
		'29'
		'9'
		'12'
		'10'
		'30'
		'9'
		'5'
		'5'
		'31'
		'12'
		'7'
		'10'
		'32'
		'7'
		'7'
		'7'
	END$TAB GEO
END$DEF DEVICE_COLOUR
BEGIN$DEF DRILL_COLOUR
	BEGIN$TAB CLI
		'@CLI'
		'#ASSAY'
		'DE'
		'ATE'
		'32'
		'AT'
		'19'
		'SO'
		'18'
		'CG'
		'13'
		'IN'
		'2'
		'HC'
		'3'
		'HF'
		'7'
		'IF'
		'6'
		'IC'
		'4'
		'HET'
		'11'
		'ITT'
		'30'
		'HMN'
		'10'
		'IMN'
		'9'
		'FM'
		'28'
		'HA'
		'22'
		'IAF'
		'18'
		'IAC'
		'25'
		'IDO'
		'16'
		'FL'
		'15'
		'QT'
	END$TAB CLI
	BEGIN$TAB FE
		'FEGL'
		'#ASSAY'
		'DE'
		'ATE'
		'1'
		'-99.000'
		'0.000'
		'12'
		'0.000'
		'25.000'
		'7'
		'25.000'
		'52.000'
		'8'
		'52.000'
		'63.000'
		'3'
		'63.000'
		'80.000'
		'GELT'
	END$TAB FE
	BEGIN$TAB LITO
		'@LITO'
		'#ASSAY'
		'FROM'
		'TO'
		''
		'C5'
		'2'
		'HC'
		'3'
		'HF'
		'28'
		'HGO'
		'8'
		'IFR'
		'7'
		'IF'
		'6'
		'IC'
		'11'
		'IGO'
		'10'
		'IMN'
		'14'
		'OC'
		'18'
		'CG'
		'32'
		'PE'
		'26'
		'LT'
		'13'
		'IN'
		'15'
		'QT'
		'17'
		'XI'
		'12'
		'RA'
		'24'
		'RR'
		'1'
		''
	END$TAB LITO
END$DEF DRILL_COLOUR
END$FILE
