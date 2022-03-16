import React from 'react'
import './index.less'
import image_map_jianye from '../../assets/images/map_jianye.png'
import image_map_donghaiwan from '../../assets/images/map_donghaiwan.png'
import image_map_jiannan from '../../assets/images/map_jiannan.png'
import image_map_changshoujiaowai from '../../assets/images/map_changshoujiaowai.png'
import image_map_qilingshan from '../../assets/images/map_qilingshan.png'




const MapConfigs = {
   '建邺城': {
       topLeft: [1, 143],
       BottomRight: [286,0],
       width: 557,
       height: 275
   },  
   '东海湾': {
        topLeft: [0, 119],
        BottomRight: [119,0],
        width: 276,
        height: 276
    }, 
    '江南野外': {
        topLeft: [0, 119],
        BottomRight: [159,0],
        width: 369,
        height: 276
    },  
    '长寿郊外': {
        topLeft: [0, 167],
        BottomRight: [191,0],
        width: 318,
        height: 276
    },
    '麒麟山': {
        topLeft: [0, 142],
        BottomRight: [190,0],
        width: 370,
        height: 278
    }, 
}

function ChMhMapTool({
    mapName,
    points
}: {
    mapName: string,
    points: [number, number][]
}) {
    // @ts-ignore
    const mapConfig = MapConfigs[mapName] || {
        topLeft: [1, 143],
        BottomRight: [286,0],
        width: 557,
        height: 275
    }

    const getRealPoint = () => {
        return points.map(point=>{
            let realPoint = [0, 0]
            let left = (mapConfig.width / (mapConfig.BottomRight[0] - mapConfig.topLeft[0])) * point[0]
            let top = (mapConfig.height / (mapConfig.topLeft[1] - mapConfig.BottomRight[1])) * point[1]
            realPoint = [left, top]
            return {
                orgPoint:point,
                realPoint
            }
        })
    }

    const getMapImage = () => {
        if(mapName === '建邺城') {
            return image_map_jianye
        } else if(mapName === '东海湾') {
            return image_map_donghaiwan
        }else if(mapName === '江南野外') {
            return image_map_jiannan
        }else if(mapName === '长寿郊外') {
            return image_map_changshoujiaowai
        }else if(mapName === '麒麟山') {
            return image_map_qilingshan
        }
        else {
            return image_map_jianye
        }
    }
    const pointDatas = getRealPoint()
    return <div className='chMhMapTool flex-center'>
        <div className='chMhMapTool-map'>
            <img width={mapConfig.width} height={mapConfig.height} src={getMapImage()} className="mh_map_jianye" />
            {
                pointDatas.map((pointData: any, index)=>{
                    let realPoint = pointData.realPoint
                    let orgPoint = pointData.orgPoint
                    return  <div key={index + '_'} style={{left: realPoint[0], bottom: realPoint[1] }}  className='chMhMapTool-map-point'> <div className='chMhMapTool-map-point-text'>
                        第{index + 1}张，坐标({orgPoint[0]}, {orgPoint[1]})
                        </div>
                    </div>
                })
            }
        </div>
    </div>
}

export default ChMhMapTool