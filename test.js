const points = [[10, 20],[15, 20],[17, 150], [5, 28]]
const firstPoint = [10, 20]
const otherPoints = points.filter(item => !(item[0] == firstPoint[0] && item[1] == firstPoint[1]))
const sortList = otherPoints.sort((group1, group2)=>{
    p1Length = Math.sqrt((group1[0] - firstPoint[0])*(group1[0] - firstPoint[0]) + (group1[1] - firstPoint[1])*(group1[1] - firstPoint[1]))
    p2Length = Math.sqrt((group1[0] - firstPoint[0])*(group2[0] - firstPoint[0]) + (group2[1] - firstPoint[1])*(group2[1] - firstPoint[1]))
    return  p1Length - p2Length
})
const ret = [firstPoint, ...sortList]
console.log(ret);