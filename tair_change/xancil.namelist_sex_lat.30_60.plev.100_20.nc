 &nam_config
  ICAL = 2,
  ISIZE = 64,
  L32BIT = .FALSE.,
  VERSION = 7.3,
  LBIGENDOUT = .TRUE.,
  LWFIO = .TRUE.,
  IWFIO_SIZE = 2048,
  NNCFILES = 1
  NCFILES = "/g/data3/w48/dm5220/ancil/user_mlevel/tair_change/sensitivity_exp/files_for_xancil/lat.30_60.plev.100_20.nc"
 /

 &nam_gridconfig
  LVARGRID = .FALSE.,
  IAVERT = 1,
  NLEV = 38,
  NO3LEV = 38,
  LLEVSTOREUP = .TRUE.,
  NAM_VERT = "/g/data/access/projects/access/umdir/vn7.3/ctldata/vert/vertlevs_G3",
  IOVERT = 0,
  LDEEPSOIL = .FALSE.
 /

 &nam_ozone
 /

 &nam_smow
 /

 &nam_slt
 /

 &nam_soil
 /

 &nam_veg
 /

 &nam_vegfrac
 /

 &nam_vegfunc
 /

 &nam_vegdist
 /

 &nam_sst
 /

 &nam_ice
 /

 &nam_orog
 /

 &nam_mask
 /

 &nam_lfrac
 /

 &nam_ausrmulti
  LAUSRMULTI = .TRUE.,
  AUSRMULTI_FILEOUT = "/g/data/w48/dm5220/ancil/user_mlevel/tair_change/sensitivity_exp/lat.30_60.plev.100_20",
  LAUSRMULTI_PERIODIC = .TRUE.,
  LAUSRMULTI_CAL_INDEP = .FALSE.,
  IAUSRMULTI_TIMEUSAGE1 = 1,
  IAUSRMULTI_TIMEUSAGE2 = 0,
  IAUSRMULTI_STARTDATE(1) = 0000,
  IAUSRMULTI_STARTDATE(2) = 1,
  IAUSRMULTI_STARTDATE(3) = 16,
  IAUSRMULTI_STARTDATE(4) = 0,
  IAUSRMULTI_STARTDATE(5) = 0,
  IAUSRMULTI_STARTDATE(6) = 0,
  IAUSRMULTI_NTIMES = 12,
  IAUSRMULTI_INTERVAL = 1,
  IAUSRMULTI_INTUNIT = 1,
  LAUSRMULTI_MM = .TRUE.
  IAUSRMULTI_NFIELD = 1
  IAUSRMULTI_FILEINID(1) = 1,
  IAUSRMULTI_STASHCODE(1) = 321,
  IAUSRMULTI_PPCODE(1) = 0,
  AUSRMULTI_NCNAME(1) = "tair_corrections",
  LAUSRMULTI_THETA(1) = .FALSE.
  IAUSRMULTI_GRIDTYPE(1) = 1,
  IAUSRMULTI_DATATYPE(1) = 1,
  IAUSRMULTI_MASKTYPE(1) = 0,
  IAUSRMULTI_MASK(1) = 0,
 /

 &nam_ausrancil
 /

 &nam_ts1
 /

 &nam_flux
 /

 &nam_ousrmulti
 /

 &nam_ousrancil
 /

 &nam_genanc_config
  NANCFILES = 1
 /

 &nam_genanc
  LGENANC_FILE(1) = .FALSE.,

 /

 &nam_astart
 /

