import numpy as np
import rasterio
from rasterio import warp

class grid_utm:
    def __init__(self, EPSG=4674):
        self.scales = [1000, 500, 250, 100, 50, 25, 10, 5, 2, 1]
        nomen1000 = []
        nomen500 = np.array([["V", "X"], ["Y", "Z"]])
        nomen250 = np.array([["A", "B"], ["C", "D"]])
        nomen100 = np.array([["I", "II", "III"], ["IV", "V", "VI"]])
        nomen50 = np.array([["1", "2"], ["3", "4"]])
        nomen25 = np.array([["NO", "NE"], ["SO", "SE"]])
        nomen10 = np.array([["A", "B"], ["C", "D"], ["E", "F"]])
        nomen5 = np.array([["I", "II"], ["III", "IV"]])
        nomen2 = np.array([["1", "2", "3"], ["4", "5", "6"]])  # map(str,range(1,7))
        nomen1 = np.array([["A", "B"], ["C", "D"]])
        self.spacingX = []
        self.spacingY = []

        self.scaleText = [
            nomen1000,
            nomen500,
            nomen250,
            nomen100,
            nomen50,
            nomen25,
            nomen10,
            nomen5,
            nomen2,
            nomen1,
        ]

    def getScaleIdFromiNomen(self, inomen):
        id = len(inomen.split("-")) - 2
        return id

    def getScale(self, inomen):
        return self.scales[self.getScaleIdFromiNomen(inomen)] * 1000

    def computeSpacingX(self):
        if len(self.spacingX) == 0:
            dx = 6.0
            self.spacingX = [dx]
            for i in range(1, len(self.scaleText)):
                subdivisions = len(self.scaleText[i][0])
                dx /= float(subdivisions)
                self.spacingX.append(dx)
        return self.spacingX

    def getSpacingX(self, scale):
        scaleId = self.scales.index(scale)
        if scaleId < 0:
            return 0
        self.computeSpacingX()
        return self.spacingX[scaleId]

    def computeSpacingY(self):
        if len(self.spacingY) == 0:
            dy = 4.0
            self.spacingY = [dy]
            for i in range(1, len(self.scaleText)):
                subdivisions = len(self.scaleText[i])
                dy /= float(subdivisions)
                self.spacingY.append(dy)
        return self.spacingY

    def getSpacingY(self, scale):
        scaleId = self.scales.index(scale)
        if scaleId < 0:
            return 0
        self.computeSpacingY()
        return self.spacingY[scaleId]

    """Main logic:
        Compute resolution
        Get nearest x size in spacingX and spacingY
        Get scale
        Get center coords 
        Compute the mod of the bin that it falls in each scale
        """

    def inomenFromExtent(self, xmin, ymin, xmax, ymax):
        inomen = ""
        fit_whole_product = False
        spacingX = np.array(self.computeSpacingX())
        spacingY = np.array(self.computeSpacingY())
        scaleX = np.argmax(spacingX <= xmax - xmin)
        scaleY = np.argmax(spacingY <= ymax - ymin)
        scale_id = min(scaleX, scaleY)
        scale = self.scales[scale_id]
        center_lat = (ymin + ymax) / 2.0
        center_lon = (xmin + xmax) / 2.0

        # 1:1.000.000 4x6
        if center_lat >= 0:
            inomen = "N"
        else:
            inomen = "S"

        def get_bin_x(lon, spacing):
            return int(np.floor((lon + 180) / spacing))  # from -180

        def get_bin_y(lat, spacing):
            return int(
                np.floor((88 - lat) / spacing)
            )  # from top 88 downward. I forgot that it must be a multiple of 4.

        row = int(np.floor(abs(center_lat / spacingY[0])))
        inomen += chr(row + 97).upper()

        zone = get_bin_x(center_lon, spacingX[0]) + 1
        inomen += f"-{zone:02d}"

        def get_inomen_part(center_lat, center_lon, calc_scale_id):
            y = get_bin_y(center_lat, spacingY[calc_scale_id])
            x = get_bin_x(center_lon, spacingX[calc_scale_id])
            calc_scale_text = self.scaleText[calc_scale_id]
            return calc_scale_text[y % len(calc_scale_text)][
                x % len(calc_scale_text[0])
            ]

        for calc_scale_id in range(1, scale_id + 1):
            text = get_inomen_part(center_lat, center_lon, calc_scale_id)
            inomen += f"-{text}"
        
        #check if it covers the entire product
        expected_extent = self.extentFromInomen(inomen)
        if (    xmin <= expected_extent[0] 
            and ymin <= expected_extent[1] 
            and xmax >= expected_extent[2] 
            and ymax >= expected_extent[3]
            ):
            return inomen
        else:
            return ""

    def getInomenFromRasterio(self, fname):
        ds = rasterio.open(fname)
        LL_bounds = warp.transform_bounds(ds.crs, 4326, *ds.bounds)
        return self.inomenFromExtent(*LL_bounds)

    def getHemisphereMultiplier(self,inomen):
        #Check hemisphere
        if (len(inomen) > 1):
            h = inomen[0].upper()
            if (h=='S'):
                return -1
            else:
                return 1
        else: 
            return 0

    #Starting latitude at scale 1:1.000.000
    def getULCornerLatitude1kk(self,inomen_part):
        l = inomen_part[1].upper()
        y = 0.0
        operator = self.getHemisphereMultiplier(inomen_part)
        verticalPosition=ord(l)-ord('A')
        y=y+4*verticalPosition*operator
        if (operator>0): y+=4
        return y

    #Starting longitude at scale 1:1.000.000 (UTM zone)
    def getULCornerLongitude1kk(self,inomen_part):
        fuso=int(inomen_part)
        x=0  
        if((fuso > 0) and (fuso <= 60)):
            x = (fuso-1)*6.0 -180.
        return x
    
    def extentFromInomen(self, inomen):
        inomen_parts = inomen.split('-')
        LLlat=LLlon=0.
        scaleId=0
        for i,inomen_part in enumerate(inomen_parts):
            if i==0:
                LLlat = self.getULCornerLatitude1kk(inomen)
            elif i==1:
                LLlon = self.getULCornerLongitude1kk(inomen_part)
            else:
                scaleId = i-1
                #TODO:this should check against bad inomen
                scaleText = np.argwhere(self.scaleText[scaleId] == inomen_part)
                if len(scaleText) == 0:
                    break #if there is a problem with the inomen, stops computation where it's still working.
                scale_div = scaleText[0]
                LLlon+=scale_div[1]*self.spacingX[scaleId]
                LLlat-=scale_div[0]*self.spacingY[scaleId]
        return(LLlon,LLlat-self.spacingY[scaleId],LLlon+self.spacingX[scaleId],LLlat)

        


if __name__ == "__main__":
    test = grid_utm()
    print(test.computeSpacingX())
    print(test.computeSpacingY())
    print(test.getSpacingX(25))

    # print(test.getInomenFromRasterio('core/test_data/recorte.tif'))
    print(
        test.getInomenFromRasterio(
            "/home/mauricio/Desktop/Doutorado_psq/PFC_2024/geometadata_creator/SCN_Carta_Topografica_Matricial-0017−2−NE-NB-22-Y-D-V-2-NE-25.000.tif"
        )
    )
    print(
        test.getInomenFromRasterio(
            "/home/mauricio/Desktop/Doutorado_psq/PFC_2024/geometadata_creator/SCN_Carta_Topografica_Matricial-PORTOALEGRE-NO-SH-22-Y-B-III-2-NO-25.000.tif"
        )
    )
    print(
        test.getInomenFromRasterio(
            "/home/mauricio/Desktop/Doutorado_psq/PFC_2024/geometadata_creator/SCN_Carta_Topografica_Matricial-PORTOALEGRE-SE-SH-22-Y-B-III-2-SE-25.000.tif"
        )
    )
