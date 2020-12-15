;------------compute the qflux-------------
;------------AUTHOR: CHEN LI---------------

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin

EXP = "vabda"

nm   = 12
nlev = 38
nlat = 73
nlon = 96

;--------------input Tsurf data---------------
;obs clim
  a = addfile("/g/data3/w48/cl7720/Ref_data/um.tsurf.12mon.climate.ERA.skt.nc","r")
  ctemp = a->tsurf
  delete(a)
 
  Qflux = ctemp
  Qflux = 0.0

; extropical
;  Qflux(:,{-90:-30},:) = 0.1
;  Qflux(:,{30:90},:) = 0.1
; tropical 
  Qflux(:,{-90:90},:)  = 1.


; Amazon
;  Qflux(:,{-10:10},{270:330}) = -50.

;land sea mask
;  a = addfile("/g/data3/w48/cl7720/Ref_data/um_slab_mask.nc","r")
;  mk = a->unspecified(:,0,:,:)
;  delete(a) 

;  do i = 0,nm-1,1
;     do j = 0,nlat-1,1
;       do k = 0,nlon-1,1
;         Qflux(i,j,k) = Qflux(i,j,k) * mk(i,j,k)
;       end do
;     end do
; end do

; ocean region
;  Qflux(:,{15:30},{160:210}) = -0.1
;  Qflux(:,{-45:-30},{60:90}) = -0.1


;rename the Atts for qtemp and make it 38 levs
  a = addfile("/g/data3/w48/cl7720/Ref_data/qflux_standard_format.nc","r")
  sd_format = a->unspecified
  
  qtemp = sd_format
  qtemp = 0.0
  do n = 0,nlev-1,1
    qtemp(:,n,:,:) =  (/Qflux/)
  end do

;change the qtemp for different levels
 coe = new((/38/),"float")
 coe = 0.0

 coe(1:2) = -0.03
 coe(3) = -0.015
 coe(4) = 0
 coe(5) = 0.05
 coe(6:8) = 0.12
 coe(9:11) = 0.06
 coe(12:17) = 0.03
 coe(18:25) = 0.05  
 

 do n = 0,nlev-1,1
 qtemp(:,n,:,:) = qtemp(:,n,:,:) * coe(n)
 end do

; don't change the upper-level air temperature in high latitude

; qtemp(:,9:,{-40:-90},:) = 0.0
; qtemp(:,9:,{40:90},:) = 0.0  

  qtemp = 0.0 

 copy_VarMeta(sd_format,qtemp)
 
;----------------- write to NetCDF----------------------

 unspecified  = qtemp

 t           = unspecified&t
 hybrid_ht   = unspecified&hybrid_ht
 latitude    = unspecified&latitude
 longitude   = unspecified&longitude

  ntim  = dimsizes(t)                 ; get dimension sizes
  nlev  = dimsizes(hybrid_ht)
  nlat  = dimsizes(latitude)
  nlon  = dimsizes(longitude)

  diro = "./"
  filo = "qflux.t.nc"
  system ("/bin/rm/ -f" + diro + filo)
  fout = addfile (diro + filo, "c")
  
  setfileoption(fout,"DefineMode",True)

        fAtt               = True            ; assign file attributes
        fAtt@title         = "NCL Efficient Approach to netCDF Creation"
        fAtt@source_file   =  "original-file.nc"
        fAtt@Conventions   = "None"
        fAtt@creation_date = systemfunc ("date")
        fileattdef( fout, fAtt )            ; copy file attributes

        dimNames = (/"t","hybrid_ht", "latitude", "longitude"/)
        dimSizes = (/ ntim   , nlev,  nlat,  nlon /)
        dimUnlim = (/ False , False, False, False/)
        filedimdef(fout,dimNames,dimSizes,dimUnlim)

       filevardef(fout, "t",typeof(t),getvardims(t))
       filevardef(fout, "hybrid_ht", typeof(hybrid_ht),getvardims(hybrid_ht))
       filevardef(fout, "latitude",typeof(latitude),getvardims(latitude))
       filevardef(fout, "longitude",typeof(longitude),getvardims(longitude))
       filevardef(fout, "unspecified",typeof(unspecified)  ,getvardims(unspecified))

;===================================================================
    ; Copy attributes associated with each variable to the file
    ; All attributes associated with each variable will be copied.
    ;====================================================================
       filevarattdef(fout,"unspecified",unspecified)                           ; copy T attributes
       filevarattdef(fout,"t" ,t)                    ; copy time attributes
       filevarattdef(fout,"hybrid_ht"  ,hybrid_ht)                     ; copy lev attributes
       filevarattdef(fout,"latitude"  ,latitude)                     ; copy lat attributes
       filevarattdef(fout,"longitude"  ,longitude)                     ; copy lon attributes

    ;===================================================================
    ; explicitly exit file definition mode. **NOT REQUIRED**
    ;===================================================================
        setfileoption(fout,"DefineMode",False)
    ;===================================================================
    ; output only the data values since the dimensionality and such have
    ; been predefined. The "(/", "/)" syntax tells NCL to only output the
    ; data values to the predefined locations on the file.
    ;====================================================================
       fout->t   = (/t/)
       fout->hybrid_ht    = (/hybrid_ht/)
       fout->latitude    = (/latitude/)
       fout->longitude    = (/longitude/)
       fout->unspecified      = (/unspecified/)

print(" OK")

end
