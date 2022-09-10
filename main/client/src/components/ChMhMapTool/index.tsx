import React, { useState } from 'react'
import { message, Switch } from 'antd'
import './index.less'
import image_map_jianye from '../../assets/images/map_jianye.png'
import image_map_donghaiwan from '../../assets/images/map_donghaiwan.png'
import image_map_jiannan from '../../assets/images/map_jiannan.png'
import image_map_changshoujiaowai from '../../assets/images/map_changshoujiaowai.png'
import image_map_qilingshan from '../../assets/images/map_qilingshan.png'
import image_map_jingwai from '../../assets/images/map_jingwai.png'
import image_map_guojing from '../../assets/images/map_guojing.png'
import image_map_mojiacun from '../../assets/images/map_mojiacun.png'
import image_map_beiju from '../../assets/images/map_beiju.png'
import image_map_putuo from '../../assets/images/map_putuo.png'
import image_map_wuzhuan from '../../assets/images/map_wuzhuan.png'
import image_map_shituo from '../../assets/images/map_shituo.png'
import image_map_zhuziguo from '../../assets/images/map_zhuziguo.png'
import image_map_huaguoshan from '../../assets/images/map_huaguoshan.png'
import image_map_aolaiguo from '../../assets/images/map_aolaiguo.png'
import image_map_nvercun from '../../assets/images/map_nvercun.png'


import { doGetWatuClickMap } from "../../call";


export const MapConfigs = {
    '建邺城': {
        topLeft: [1, 143],
        BottomRight: [286, 0],
        width: 557,
        height: 275
    },
    '东海湾': {
        topLeft: [0, 119],
        BottomRight: [119, 0],
        width: 276,
        height: 276
    },
    '江南野外': {
        topLeft: [0, 119],
        BottomRight: [159, 0],
        width: 369,
        height: 276
    },
    '长寿郊外': {
        topLeft: [0, 167],
        BottomRight: [191, 0],
        width: 318,
        height: 276
    },
    '麒麟山': {
        topLeft: [0, 142],
        BottomRight: [190, 0],
        width: 370,
        height: 278
    },
    '大唐境外': {
        topLeft: [0, 119],
        BottomRight: [638, 0],
        width: 585,
        height: 108
    },
    '大唐国境': {
        topLeft: [0, 335],
        BottomRight: [351, 0],
        width: 378,
        height: 360
    },
    '墨家村': {
        topLeft: [0, 167],
        BottomRight: [95, 0],
        width: 194,
        height: 341
    },
    '北俱芦洲': {
        topLeft: [0, 169],
        BottomRight: [227, 0],
        width: 367,
        height: 279
    },
    '普陀山': {
        topLeft: [0, 71],
        BottomRight: [95, 0],
        width: 372,
        height: 277
    },
    '五庄观': {
        topLeft: [0, 74],
        BottomRight: [99, 0],
        width: 377,
        height: 278
    },
    '狮驼岭': {
        topLeft: [0, 98],
        BottomRight: [131, 0],
        width: 370,
        height: 276
    },
    '朱紫国': {
        topLeft: [0, 119],
        BottomRight: [190, 0],
        width: 440,
        height: 276
    }, '花果山': {
        topLeft: [0, 119],
        BottomRight: [159, 0],
        width: 368,
        height: 276
    }, '傲来国': {
        topLeft: [0, 150],
        BottomRight: [221, 0],
        width: 410,
        height: 277
    }, '女儿村': {
        topLeft: [0, 143],
        BottomRight: [127, 0],
        width: 320,
        height: 362
    },
}

function ChMhMapTool({
    deviceId,
    mapName,
    points,
    cangkuPath
}: {
    deviceId: number,
    mapName: string,
    points: [number, number][]
    cangkuPath: string,
}) {
    // @ts-ignore
    const mapConfig = MapConfigs[mapName] || {
        topLeft: [1, 143],
        BottomRight: [286, 0],
        width: 557,
        height: 275
    }
    const [mulMode, setMulMode] = useState(true)
    const getRealPoint = () => {
        // let _points = points.filter(item => !(item[0] == 0 && item[1] == 0))
        let _points = points
        return _points.map(point => {
            let realPoint = [0, 0]
            let left = (mapConfig.width / (mapConfig.BottomRight[0] - mapConfig.topLeft[0])) * point[0]
            let top = (mapConfig.height / (mapConfig.topLeft[1] - mapConfig.BottomRight[1])) * point[1]
            if (left < 0 || left > mapConfig.width) {
                left = 0
            }
            if (top < 0 || top > mapConfig.height) {
                left = 0
            }
            realPoint = [left, top]
            return {
                orgPoint: point,
                realPoint
            }
        })
    }
    const getMapImage = () => {
        if (mapName === '建邺城') {
            return image_map_jianye
        } else if (mapName === '东海湾') {
            return image_map_donghaiwan
        } else if (mapName === '江南野外') {
            return image_map_jiannan
        } else if (mapName === '长寿郊外') {
            return image_map_changshoujiaowai
        } else if (mapName === '麒麟山') {
            return image_map_qilingshan
        }
        else if (mapName === '大唐境外') {
            return image_map_jingwai
        }
        else if (mapName === '大唐国境') {
            return image_map_guojing
        } else if (mapName === '墨家村') {
            return image_map_mojiacun
        } else if (mapName === '北俱芦洲') {
            return image_map_beiju
        }
        else if (mapName === '普陀山') {
            return image_map_putuo
        } else if (mapName === '五庄观') {
            return image_map_wuzhuan
        } else if (mapName === '狮驼岭') {
            return image_map_shituo
        } else if (mapName === '朱紫国') {
            return image_map_zhuziguo
        } else if (mapName === '花果山') {
            return image_map_huaguoshan
        } else if (mapName === '傲来国') {
            return image_map_aolaiguo
        } else if (mapName === '女儿村') {
            return image_map_nvercun
        }
        else {
            return image_map_jianye
        }
    }
    const pointDatas = getRealPoint()

    const handleClickPoint = (map: string, realX: number, realY: number, orgPointX: number, orgPointY: number, index: number) => {
        const x = Math.round(realX)
        const y = Math.round(realY)
        if (mulMode) {
            let otherPoint = pointDatas.map((item, i) => {
                return {
                    realX: Math.round(item.realPoint[0]),
                    realY: Math.round(mapConfig.height - item.realPoint[1]),
                    orgPointX: item.orgPoint[0],
                    orgPointY: item.orgPoint[1],
                    index: i + 1,
                }
            })
            otherPoint.splice(index - 1, 1)
            let otherJson = JSON.stringify(otherPoint)
            // @ts-ignore
            doGetWatuClickMap(mapName, x, y, orgPointX, orgPointY, index, otherJson, window.isBee, cangkuPath, window.isChilan)
        } else {
            // @ts-ignore
            doGetWatuClickMap(mapName, x, y, orgPointX, orgPointY, index, undefined, window.isBee, cangkuPath, window.isChilan)
        }
    }

    const handleClickArgs = (map: string, realX: number, realY: number, orgPointX: number, orgPointY: number, index: number) => {
        const x = Math.round(realX)
        const y = Math.round(realY)
        let otherPoint = pointDatas.map((item, i) => {
            return {
                realX: Math.round(item.realPoint[0]),
                realY: Math.round(mapConfig.height - item.realPoint[1]),
                orgPointX: item.orgPoint[0],
                orgPointY: item.orgPoint[1],
                index: i + 1,
            }
        })
        otherPoint.splice(index - 1, 1)
        let otherJson = JSON.stringify(otherPoint)
        return [mapName, x, y, orgPointX, orgPointY, index, otherJson]
    }

    return <div>
        {/* <br />
        <div>
            <span style={{ color: '#000' }}>是否群挖</span>： <Switch checked={mulMode} onChange={(e) => setMulMode(e)} />
        </div>

        <br /> */}
        <div key={mapName + '_watu'} className='chMhMapTool flex-center'>
            <div className='chMhMapTool-map'>
                <img width={mapConfig.width} height={mapConfig.height} src={getMapImage()} className="mh_map_jianye" />
                {
                    pointDatas.map((pointData: any, index) => {
                        let realPoint = pointData.realPoint
                        let orgPoint = pointData.orgPoint
                        if (index == 0) {
                            // @ts-ignore
                            window.beeData = handleClickArgs(mapName, realPoint[0], mapConfig.height - realPoint[1], orgPoint[0], orgPoint[1], index + 1, true)
                        }
                        return <div id={`${mapName}${index}`} onClick={() => {
                            handleClickPoint(mapName, realPoint[0], mapConfig.height - realPoint[1], orgPoint[0], orgPoint[1], index + 1)
                            const dom = window.document.querySelector(`#${mapName}${index}`)
                            // @ts-ignore
                            dom!.style['background-color'] = '#fff'
                            message.info(
                                `第${index + 1}张，坐标(${orgPoint[0]}, ${orgPoint[1]})`, 20)
                        }} key={mapName + index + '_'} style={{ left: realPoint[0], bottom: realPoint[1] }} className='chMhMapTool-map-point'>
                        </div>
                    })
                }
            </div>
        </div>
    </div>
}

export default ChMhMapTool