def sort_dict(unsorted_dict: dict) -> dict:
    return {key: value for key, value in sorted(unsorted_dict.items(), key=lambda item: item[0])}


def get_path_dict(modus: tuple = (-1, -1)) -> dict:

    image_dict = {}

    if 0 in modus:  # dirt
        print("dirt")
        image_dict.update({
            'dirtCenter.png': 0,
            'dirtCenter_rounded.png': 1,
            'dirtCliffLeft.png': 2,
            'dirtCliffLeftAlt.png': 3,
            'dirtCliffRight.png': 4,
            'dirtCliffRightAlt.png': 5,
            'dirtHalf.png': 6,
            'dirtHalfLeft.png': 7,
            'dirtHalfMid.png': 8,
            'dirtHalfRight.png': 9,
            'dirtHillLeft.png': 10,
            'dirtHillLeft2.png': 11,
            'dirtHillRight.png': 12,
            'dirtHillRight2.png': 13,
            'dirtLeft.png': 14,
            'dirtMid.png': 15,
            'dirtRight.png': 16})
    if 1 in modus:
        print("dirt enhanced")
        image_dict.update({
            'dirt.png': 100,
            'dirtCaveBL.png': 101,
            'dirtCaveBR.png': 102,
            'dirtCaveBottom.png': 103,
            'dirtCaveSpikeBottom.png': 104,
            'dirtCaveSpikeTop.png': 105,
            'dirtCaveTop.png': 106,
            'dirtCaveUL.png': 107,
            'dirtCaveUR.png': 108,
        })
    if 2 in modus:  # Stone
        print("stone")
        image_dict.update({
            'stone.png': 200,
            'stoneCaveBL.png': 201,
            'stoneCaveBR.png': 202,
            'stoneCaveBottom.png': 203,
            'stoneCaveRockLarge.png': 204,
            'stoneCaveRockSmall.png': 205,
            'stoneCaveSpikeBottom.png': 206,
            'stoneCaveSpikeTop.png': 207,
            'stoneCaveTop.png': 208,
            'stoneCaveUL.png': 209,
            'stoneCaveUR.png': 210,
            'stoneCenter.png': 211,
            'stoneCenter_rounded.png': 212,
            'stoneCliffLeft.png': 213,
            'stoneCliffLeftAlt.png': 213,
            'stoneCliffRight.png': 0,
            'stoneCliffRightAlt.png': 0,
            'stoneHalf.png': 0,
            'stoneHalfLeft.png': 0,
            'stoneHalfMid.png': 0,
            'stoneHalfRight.png': 0,
            'stoneHillLeft2.png': 0,
            'stoneHillRight2.png': 0,
            'stoneLeft.png': 0,
            'stoneMid.png': 0,
            'stoneRight.png': 0,
            'stoneWall.png': 0,
            'rockHillLeft.png': 0,
            'rockHillRight.png': 0,
        })
    if 3 in modus:  # sand
        print("sand")
        image_dict.update({
            'sand.png': 0,
            'sandCenter.png': 0,
            'sandCenter_rounded.png': 0,
            'sandCliffLeft.png': 0,
            'sandCliffLeftAlt.png': 0,
            'sandCliffRight.png': 0,
            'sandCliffRightAlt.png': 0,
            'sandHalf.png': 0,
            'sandHalfLeft.png': 0,
            'sandHalfMid.png': 0,
            'sandHalfRight.png': 0,
            'sandHillLeft.png': 0,
            'sandHillLeft2.png': 0,
            'sandHillRight.png': 0,
            'sandHillRight2.png': 0,

            'sandLeft.png': 0,
            'sandMid.png': 0,
            'sandRight.png': 0
        })
    if 4 in modus:  # snow
        print("snow")
        image_dict.update({
            'snow.png': 0,
            'snowCenter.png': 0,
            'snowCenter_rounded.png': 0,
            'snowCliffLeft.png': 0,
            'snowCliffLeftAlt.png': 0,
            'snowCliffRight.png': 0,
            'snowCliffRightAlt.png': 0,
            'snowHalf.png': 0,
            'snowHalfLeft.png': 0,
            'snowHalfMid.png': 0,
            'snowHalfRight.png': 0,
            'snowHillLeft.png': 0,
            'snowHillLeft2.png': 0,
            'snowHillRight.png': 0,
            'snowHillRight2.png': 0,

            'snowLeft.png': 0,
            'snowMid.png': 0,
            'snowRight.png': 0,
        })
    if 5 in modus:  # castle
        print("castle")
        image_dict.update({
            'castle.png': 0,
            'castleCenter.png': 0,
            'castleCenter_rounded.png': 0,
            'castleCliffLeft.png': 0,
            'castleCliffLeftAlt.png': 0,
            'castleCliffRight.png': 0,
            'castleCliffRightAlt.png': 0,
            'castleHalf.png': 0,
            'castleHalfLeft.png': 0,
            'castleHalfMid.png': 0,
            'castleHalfRight.png': 0,
            'castleHillLeft.png': 0,
            'castleHillLeft2.png': 0,
            'castleHillRight.png': 0,
            'castleHillRight2.png': 0,
            'castleLeft.png': 0,
            'castleMid.png': 0,
            'castleRight.png': 0,
        })

    if 6 in modus:  # metal
        print("metal")
        image_dict.update({
            'metal.png': 0,
            'metalCenter.png': 0,
            'metalCenterSticker.png': 0,
            'metalCenterWarning.png': 0,
            'metalCliffLeft.png': 0,
            'metalCliffLeftAlt.png': 0,
            'metalCliffRight.png': 0,
            'metalCliffRightAlt.png': 0,
            # 'metalFence.png': 0,
            # 'metalFenceAlt.png': 0,
            'metalHalf.png': 0,
            'metalHalfLeft.png': 0,
            'metalHalfMid.png': 0,
            'metalHalfRight.png': 0,
            'metalLeft.png': 0,
            'metalMid.png': 0,
            'metalPlatform.png': 0,
            'metalPlatformWire.png': 0,
            'metalPlatformWireAlt.png': 0,
            'metalRight.png': 0,
            'metalRounded.png': 0,
            'tile_20.png': 0,
            'tile_21.png': 0,
        })
    if 7 in modus:
        print("gras")
        image_dict.update({
            'grass.png': 0,
            'grassCenter.png': 0,
            'grassCenter_rounded.png': 0,
            'grassCliffLeft.png': 0,
            'grassCliffLeftAlt.png': 0,
            'grassCliffRight.png': 0,
            'grassCliffRightAlt.png': 0,
            'grassHalf.png': 0,
            'grassHalfLeft.png': 0,
            'grassHalfMid.png': 0,
            'grassHalfRight.png': 0,
            'grassHillLeft.png': 0,
            'grassHillLeft2.png': 0,
            'grassHillRight.png': 0,
            'grassHillRight2.png': 0,
            'grassLeft.png': 0,
            'grassMid.png': 0,
            'grassRight.png': 0,
        })

    if 10 in modus:
        print("items")
        image_dict.update({
            'bomb.png': 0,

            'bush.png': 0,
            'cactus.png': 0,
            'coinBronze.png': 0,
            'coinSilver.png': 0,
            'coinGold.png': 0,
            'rock.png': 0,


            'mushroomBrown.png': 0,
            'mushroomRed.png': 0,
            'plant.png': 0,
            'plantPurple.png': 0,

            'flagBlue.png': 0,
            'flagBlue2.png': 0,
            'flagBlueHanging.png': 0,
            # 'gemBlue.png': 0,
            'gemGreen.png': 0,
            # 'gemRed.png': 0,
            # 'gemYellow.png': 0,

            'ladder_mid.png': 0,
            'ladder_top.png': 0,

            'spikes.png': 0,
            'springboardDown.png': 0,
            'springboardUp.png': 0,

            'switchLeft.png': 0,
            'switchMid.png': 0,
            'switchRight.png': 0,
            'torch.png': 0,
            'torchLit.png': 0,
            'torchLit2.png': 0,
            # 'weight.png': 0,
            # 'weightChained.png': 0,
            'umbrellaClosed.png': 0,
            'umbrellaOpen.png': 0
        })
    if 11 in modus:
        print("sp tiles")
        image_dict.update({
            'door_closedMid.png': 0,
            'door_closedTop.png': 0,
            'door_openMid.png': 0,
            'door_openTop.png': 0,
            'fence.png': 0,
            'fenceBroken.png': 0,
            'box.png': 0,
            'boxAlt.png': 0,
            'brickWall.png': 0,
            'bridgeLogs.png': 0,
            'sign.png': 0,
            'signExit.png': 0,
            'signLeft.png': 0,
            'signRight.png': 0,
            'window.png': 0,
            'wireBottomLeft.png': 0,
            'wireBottomRight.png': 0,
            'wireHook.png': 0,
            'wireLeft.png': 0,
            'wireRight.png': 0

        })

    if 12 in modus:
        print("liquids")
        image_dict.update({
            'liquidLava.png': 0,
            'liquidLavaTop.png': 0,
            'liquidLavaTop_mid.png': 0,
            'liquidWater.png': 0,
            'liquidWaterTop.png': 0,
            'liquidWaterTop_mid.png': 0,
        })

    return sort_dict(image_dict)
