WAD_EXTRACT = 'Tools/lcs-manager/cslol-tools/wad-extract.exe'
WAD_MAKE = 'Tools/lcs-manager/cslol-tools/wad-make.exe'
RITO_BIN = 'Tools/ritobin/bin/ritobin_cli.exe'
TEX2DDS = 'Tools/tex2dds.exe'
SKL_CONVERT = 'Tools/skl-convert.exe'

BIN_ANALYZE = ["VfxSystemDefinitionData", "emitterName", "Texture", "mSimpleMeshName", "particleName", "particlePath", "soundOnCreateDefault"]
BIN_ANALYZE_DOUBLETAB = ["Texture", "mSimpleMeshName", "particleName", "particlePath", "soundOnCreateDefault"]

def update_vfx_name(vfx):
    if vfx.lower() == "Yasuo_W_windwall_big_impact".lower():
        vfx = "Yasuo_Base_W_windwall_big_impact"
    return vfx