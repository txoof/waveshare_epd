#!/usr/bin/env python3
# coding: utf-8








# import epdconfig






# epdconfig = epdconfig.RaspberryPi()






import logging
try:
    from . import epdconfig
except ImportError:
    import epdconfig






# Constants
EPD_WIDTH = 176
EPD_HEIGHT = 264

# colors
GRAY1  = 0xff #white
GRAY2  = 0xC0
GRAY3  = 0x80 #gray
GRAY4  = 0x00 #Blackest






# Display resolution
class EPD:
    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.GRAY1  = GRAY1 #white
        self.GRAY2  = GRAY2
        self.GRAY3  = GRAY3 #gray
        self.GRAY4  = GRAY4 #Blackest

    # lookup tables
    lut_vcom_dc = [0x00, 0x00,
        0x00, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x60, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x00, 0x14, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]
    
    # white to white transition
    lut_ww = [
        0x40, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x40, 0x14, 0x00, 0x00, 0x00, 0x01,
        0xA0, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    
    # black to white transition
    lut_bw = [
        0x40, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x40, 0x14, 0x00, 0x00, 0x00, 0x01,
        0xA0, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    
    # black to black transition
    lut_bb = [
        0x80, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x80, 0x14, 0x00, 0x00, 0x00, 0x01,
        0x50, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    
    # white to black transition
    lut_wb = [
        0x80, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x80, 0x14, 0x00, 0x00, 0x00, 0x01,
        0x50, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    ###################full screen update LUT######################
    #0~3 gray
    
    gray_lut_vcom = [
        0x00, 0x00,
        0x00, 0x0A, 0x00, 0x00, 0x00, 0x01,
        0x60, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x00, 0x14, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x13, 0x0A, 0x01, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    
    #R21
    gray_lut_ww =[
        0x40, 0x0A, 0x00, 0x00, 0x00, 0x01,
        0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x10, 0x14, 0x0A, 0x00, 0x00, 0x01,
        0xA0, 0x13, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    
    #R22H r
    gray_lut_bw =[
        0x40, 0x0A, 0x00, 0x00, 0x00, 0x01,
        0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x00, 0x14, 0x0A, 0x00, 0x00, 0x01,
        0x99, 0x0C, 0x01, 0x03, 0x04, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    
    #R23H w
    gray_lut_wb =[
        0x40, 0x0A, 0x00, 0x00, 0x00, 0x01,
        0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x00, 0x14, 0x0A, 0x00, 0x00, 0x01,
        0x99, 0x0B, 0x04, 0x04, 0x01, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    
    #R24H b
    gray_lut_bb =[
        0x80, 0x0A, 0x00, 0x00, 0x00, 0x01,
        0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x20, 0x14, 0x0A, 0x00, 0x00, 0x01,
        0x50, 0x13, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    
#     # Hardware reset
    def reset(self):
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200) 
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(5)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(200)   

    def send_command(self, command):
        epdconfig.digital_write(self.dc_pin, 0)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([command])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([data])
        epdconfig.digital_write(self.cs_pin, 1)
        
    #### REVIEW ####
    # consider making a break/raise after N loops of attempting to release busy status
    def ReadBusy(self):
        logging.debug("e-Paper busy")
        while(epdconfig.digital_read(self.busy_pin) == 0):      #  0: idle, 1: busy
            epdconfig.delay_ms(200)
        logging.debug("e-Paper busy release")

    def set_lut(self):
        self.send_command(0x20) # vcom
        for count in range(0, 44):
            self.send_data(self.lut_vcom_dc[count])
        self.send_command(0x21) # ww --
        for count in range(0, 42):
            self.send_data(self.lut_ww[count])
        self.send_command(0x22) # bw r
        for count in range(0, 42):
            self.send_data(self.lut_bw[count])
        self.send_command(0x23) # wb w
        for count in range(0, 42):
            self.send_data(self.lut_bb[count])
        self.send_command(0x24) # bb b
        for count in range(0, 42):
            self.send_data(self.lut_wb[count])
            
#     def set_lut_gray(self):
    def gray_SetLut(self):
        self.send_command(0x20)
        for count in range(0, 44):        #vcom
            self.send_data(self.gray_lut_vcom[count])
            
        self.send_command(0x21) #red not use
        for count in range(0, 42): 
            self.send_data(self.gray_lut_ww[count])

        self.send_command(0x22) #bw r
        for count in range(0, 42): 
            self.send_data(self.gray_lut_bw[count])

        self.send_command(0x23) #wb w
        for count in range(0, 42): 
            self.send_data(self.gray_lut_wb[count])

        self.send_command(0x24) #bb b
        for count in range(0, 42): 
            self.send_data(self.gray_lut_bb[count])

        self.send_command(0x25)	 #vcom
        for count in range(0, 42): 
            self.send_data(self.gray_lut_ww[count])

   
    def init(self):
        logging.info('init EPD screen (Black & White)')
        if (epdconfig.module_init() != 0):
            return -1
        self.reset()
        
        # see pp35: https://www.waveshare.com/w/upload/2/2d/2.7inch-e-paper-Specification.pdf
        logging.debug('booster soft start')
        self.send_command(0x06) # BOOSTER_SOFT_START see PP13-14
        self.send_data(0x07) # PHA
        self.send_data(0x07) # PHB 
        self.send_data(0x17) # PHC
            
        # poorly documented -- unclear what this does
        # see https://github.com/waveshare/e-Paper/issues/155
        logging.debug('power optimization stages 1-4')
        # Power optimization stage 1
        self.send_command(0xF8)
        self.send_data(0x60)
        self.send_data(0xA5)
        
        # Power optimization stage 2
        self.send_command(0xF8)
        self.send_data(0x89)
        self.send_data(0xA5)
        
        # Power optimization stage 3
        self.send_command(0xF8)
        self.send_data(0x90)
        self.send_data(0x00)
        
        # Power optimization stage 4
        self.send_command(0xF8)
        self.send_data(0x93)
        self.send_data(0x2A)        
            
        
        logging.debug('reset DFV_EN')
        self.send_command(0x16) # PARTIAL_DISPLAY_REFRESH
        self.send_data(0x00)
        
        logging.debug('power setting')
        self.send_command(0x01) # POWER_SETTING
        self.send_data(0x03) # VDS_EN, VDG_EN
        self.send_data(0x00) # VCOM_HV, VGHL_LV[1], VGHL_LV[0]
        self.send_data(0x2b) # VDH
        self.send_data(0x2b) # VDL
#         self.send_data(0x09) # VDHR -- set voltage for red pixel (uneeded in B&W)
        
        
        logging.debug('power on')
        self.send_command(0x04) # POWER_ON
        self.ReadBusy()
        
        logging.debug('pannel setting')
        self.send_command(0x00) # PANEL_SETTING (see p11)
        self.send_data(0xAF) # res 296x160, use LUT, USE B/W/R pixels, scan up, shift rt, booster on, booster off
        
        logging.debug('PLL control frequency setting (100Hz)')
        self.send_command(0x30) # PLL_CONTROL
        self.send_data(0x3A) # 3A 100HZ   29 150Hz 39 200HZ    31 171HZ
        
        logging.debug('resolution setting (176x264)')
        self.send_command(0x61)
        self.send_data(0x00) #176
        self.send_data(0xb0) 
        self.send_data(0x01) #264
        self.send_data(0x08)
        
        # order of VCOM and VCM_DC is swapped in spec; must be swapped as shown below
        logging.debug('Vcom and data interval setting')
        self.send_command(0X50) #VCOM AND DATA INTERVAL SETTING
        self.send_data(0x57) # 0x57 in original code
        
        logging.debug('VCM_DC setting ')       
        self.send_command(0x82) # VCM_DC_SETTING_REGISTER
        self.send_data(0x12)
        
        logging.debug('set b&w lookup tables')
        self.set_lut()
        
        return 0

    def Init_4Gray(self):
        logging.info('init EPD screen (4Gray & White)')
        if (epdconfig.module_init() != 0):
            return -1
        self.reset()
        
        logging.debug('booster soft start')
        self.send_command(0x06) # BOOSTER_SOFT_START see PP13-14
        self.send_data(0x07) # PHA
        self.send_data(0x07) # PHB 
        self.send_data(0x17) # PHC

        # poorly documented -- unclear what this does
        # see https://github.com/waveshare/e-Paper/issues/155
        logging.debug('power optimization stages 1-4')
        # Power optimization stage 1
        self.send_command(0xF8)
        self.send_data(0x60)
        self.send_data(0xA5)
        
        # Power optimization stage 2
        self.send_command(0xF8)
        self.send_data(0x89)
        self.send_data(0xA5)
        
        # Power optimization stage 3
        self.send_command(0xF8)
        self.send_data(0x90)
        self.send_data(0x00)
        
        # Power optimization stage 4
        self.send_command(0xF8)
        self.send_data(0x93)
        self.send_data(0x2A)      

        logging.debug('reset DFV_EN')
        self.send_command(0x16) # PARTIAL_DISPLAY_REFRESH
        self.send_data(0x00)    

        logging.debug('power setting')
        self.send_command(0x01) # POWER_SETTING
        self.send_data(0x03) # VDS_EN, VDG_EN
        self.send_data(0x00) # VCOM_HV, VGHL_LV[1], VGHL_LV[0]
        self.send_data(0x2b) # VDH
        self.send_data(0x2b) # VDL

        logging.debug('power on')
        self.send_command(0x04) # POWER_ON
        self.ReadBusy()

        logging.debug('pannel setting')
        self.send_command(0x00) # PANEL_SETTING (see p13)
        self.send_data(0xbf) # res 296z160, use LUT, use BW pixles LUT1, scan up, shift rt, booster on, booster off
     
        logging.debug('PLL control frequency setting')
        self.send_command(0x30) # PLL_CONTROL
        self.send_data(0x90) # original from code 100Hz?

        logging.debug('resolution setting (176x264)')
        self.send_command(0x61)
        self.send_data(0x00) #176
        self.send_data(0xb0) 
        self.send_data(0x01) #264
        self.send_data(0x08)

        # order of VCOM and VCM_DC is swapped in spec; must be swapped as shown below
        logging.debug('Vcom and data interval setting')
        self.send_command(0X50) #VCOM AND DATA INTERVAL SETTING
        self.send_data(0x57) # 0x57 in original code

        logging.debug('VCM_DC setting ')       
        self.send_command(0x82) # VCM_DC_SETTING_REGISTER
        self.send_data(0x12)         
        
        return 0 


    def getbuffer(self, image):
        # logging.debug("bufsiz = ",int(self.width/8) * self.height)
        buf = [0xFF] * (int(self.width/8) * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        # logging.debug("imwidth = %d, imheight = %d",imwidth,imheight)
        if(imwidth == self.width and imheight == self.height):
            logging.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        elif(imwidth == self.height and imheight == self.width):
            logging.debug("Horizontal")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[int((newx + newy*self.width) / 8)] &= ~(0x80 >> (y % 8))
        return buf

    def getbuffer_4Gray(self, image):
        # logging.debug("bufsiz = ",int(self.width/8) * self.height)
        buf = [0xFF] * (int(self.width / 4) * self.height)
        image_monocolor = image.convert('L')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        i=0
        # logging.debug("imwidth = %d, imheight = %d",imwidth,imheight)
        if(imwidth == self.width and imheight == self.height):
            logging.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if(pixels[x, y] == 0xC0):
                        pixels[x, y] = 0x80
                    elif (pixels[x, y] == 0x80):
                        pixels[x, y] = 0x40
                    i= i+1
                    if(i%4 == 0):
                        buf[int((x + (y * self.width))/4)] = ((pixels[x-3, y]&0xc0) | (pixels[x-2, y]&0xc0)>>2 | (pixels[x-1, y]&0xc0)>>4 | (pixels[x, y]&0xc0)>>6)
                        
        elif(imwidth == self.height and imheight == self.width):
            logging.debug("Horizontal")
            for x in range(imwidth):
                for y in range(imheight):
                    newx = y
                    newy = x
                    if(pixels[x, y] == 0xC0):
                        pixels[x, y] = 0x80
                    elif (pixels[x, y] == 0x80):
                        pixels[x, y] = 0x40
                    i= i+1
                    if(i%4 == 0):
                        buf[int((newx + (newy * self.width))/4)] = ((pixels[x, y-3]&0xc0) | (pixels[x, y-2]&0xc0)>>2 | (pixels[x, y-1]&0xc0)>>4 | (pixels[x, y]&0xc0)>>6) 
        return buf


    def display(self, image):
        # load image into buffer
        self.send_command(0x10) # start transmission 1
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)
        self.send_command(0x13) # start transmisison 2
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(image[i])
        # write buffer to display
        self.send_command(0x12) # display refresh
        self.ReadBusy()

    def display_4Gray(self, image):
        self.send_command(0x10)
        for i in range(0, 5808):                     #5808*4  46464
            temp3=0
            for j in range(0, 2):
                temp1 = image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0xC0 
                    if(temp2 == 0xC0):
                        temp3 |= 0x01#white
                    elif(temp2 == 0x00):
                        temp3 |= 0x00  #black
                    elif(temp2 == 0x80): 
                        temp3 |= 0x01  #gray1
                    else: #0x40
                        temp3 |= 0x00 #gray2
                    temp3 <<= 1	
                    
                    temp1 <<= 2
                    temp2 = temp1&0xC0 
                    if(temp2 == 0xC0):  #white
                        temp3 |= 0x01
                    elif(temp2 == 0x00): #black
                        temp3 |= 0x00
                    elif(temp2 == 0x80):
                        temp3 |= 0x01 #gray1
                    else :   #0x40
                            temp3 |= 0x00	#gray2	
                    if(j!=1 or k!=1):				
                        temp3 <<= 1
                    temp1 <<= 2
            self.send_data(temp3)
            
        self.send_command(0x13)	       
        for i in range(0, 5808):                #5808*4  46464
            temp3=0
            for j in range(0, 2):
                temp1 = image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0xC0 
                    if(temp2 == 0xC0):
                        temp3 |= 0x01#white
                    elif(temp2 == 0x00):
                        temp3 |= 0x00  #black
                    elif(temp2 == 0x80):
                        temp3 |= 0x00  #gray1
                    else: #0x40
                        temp3 |= 0x01 #gray2
                    temp3 <<= 1	
                    
                    temp1 <<= 2
                    temp2 = temp1&0xC0 
                    if(temp2 == 0xC0):  #white
                        temp3 |= 0x01
                    elif(temp2 == 0x00): #black
                        temp3 |= 0x00
                    elif(temp2 == 0x80):
                        temp3 |= 0x00 #gray1
                    else:    #0x40
                            temp3 |= 0x01	#gray2
                    if(j!=1 or k!=1):					
                        temp3 <<= 1
                    temp1 <<= 2
            self.send_data(temp3)
        
        self.gray_SetLut()
        self.send_command(0x12)
        epdconfig.delay_ms(200)
        self.ReadBusy()
        # pass

    
    #### REVIEW ####
    # color arg is not needed -- keep for consistency between color and non-color models?
    def Clear(self, color):
        # send blank (0xFF) into buffer
        self.send_command(0x10) # start data transmission 1
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)
        # send blank (0xFF) into buffer            
        self.send_command(0x13) # start data transmission 2
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)
        # write buffer to display
        self.send_command(0x12) # display refresh
        self.ReadBusy()

    def sleep(self):
        logging.info('enter sleep')
        self.send_command(0X50) # Vcom and data interval setting
        self.send_data(0xf7)
        logging.debug('power off')
        self.send_command(0X02) # power off
        logging.debug('enter deep sleep')
        self.send_command(0X07) # deep sleep
        self.send_data(0xA5) #deep sleep
        epdconfig.delay_ms(2000)
        epdconfig.module_exit()
### END OF FILE ###






# from pathlib import Path
# import time
# from PIL import Image,ImageDraw,ImageFont

# import logging
# logging.root.setLevel('INFO')

# font_file = str(Path('../../pic/Font.ttc').resolve())
# pic = Path('../../pic/2in7.bmp')
# picH = Path('../../pic/2in7_Scale.bmp')

# epd = EPD()
# epd.init()
# # epd.Clear(0xFF)

# epd.init()

# font24 = ImageFont.truetype(font_file, 24)
# font18 = ImageFont.truetype(font_file, 18)
# font35 = ImageFont.truetype(font_file, 35)
# # Drawing on the Horizontal image
# logging.info("1.Drawing on the Horizontal image...")
# Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
# draw = ImageDraw.Draw(Himage)
# draw.text((10, 0), 'hello world', font = font24, fill = 0)
# draw.text((150, 0), u'微雪电子', font = font24, fill = 0)    
# draw.line((20, 50, 70, 100), fill = 0)
# draw.line((70, 50, 20, 100), fill = 0)
# draw.rectangle((20, 50, 70, 100), outline = 0)
# draw.line((165, 50, 165, 100), fill = 0)
# draw.line((140, 75, 190, 75), fill = 0)
# draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
# draw.rectangle((80, 50, 130, 100), fill = 0)
# draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
# epd.display(epd.getbuffer(Himage))
# time.sleep(2)

# Himage = Image.open(pic)
# epd.display(epd.getbuffer(Himage))

# '''4Gray display'''
# logging.info("4Gray display--------------------------------")
# epd.Init_4Gray()

# Limage = Image.new('L', (epd.width, epd.height), 0)  # 255: clear the frame
# draw = ImageDraw.Draw(Limage)
# draw.text((20, 0), u'微雪电子', font = font35, fill = epd.GRAY1)
# draw.text((20, 35), u'微雪电子', font = font35, fill = epd.GRAY2)
# draw.text((20, 70), u'微雪电子', font = font35, fill = epd.GRAY3)
# draw.text((40, 110), 'hello world', font = font18, fill = epd.GRAY1)
# draw.line((10, 140, 60, 190), fill = epd.GRAY1)
# draw.line((60, 140, 10, 190), fill = epd.GRAY1)
# draw.rectangle((10, 140, 60, 190), outline = epd.GRAY1)
# draw.line((95, 140, 95, 190), fill = epd.GRAY1)
# draw.line((70, 165, 120, 165), fill = epd.GRAY1)
# draw.arc((70, 140, 120, 190), 0, 360, fill = epd.GRAY1)
# draw.rectangle((10, 200, 60, 250), fill = epd.GRAY1)
# draw.chord((70, 200, 120, 250), 0, 360, fill = epd.GRAY1)
# epd.display_4Gray(epd.getbuffer_4Gray(Limage))
# time.sleep(2)

# #display 4Gra bmp
# Himage = Image.open(picH)
# epd.display_4Gray(epd.getbuffer_4Gray(Himage))
# time.sleep(2)


# logging.info("Clear...")
# epd.Clear(0xFF)
# logging.info("Goto Sleep...")
# epd.sleep()    
















