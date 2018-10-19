import cadquery as cq
from Helpers import show

ringHeight = 7.6
ringWidth = 4.6
ringTopWidth = 2.0
ringTopSpaceHeight = 2.5
ringBottomSpaceHeight = 0.8
ringThickness = 1.3
ringRadius = 31.0
ringSupporterNumber = 13
ringSupporterThickness = 1.0

holderBaseRadius = 9.8 / 2
holderBaseHeight = ringWidth
holderFookRadius = 3.7 / 2
holderFookHeight = 5.0
holderStopperWidth = 1.4
holderStopperHeight = 1.2
holderStopperLength = 0.8

jointBaseRadius = 12.0 / 2
jointBaseHeight = 2.0
jointBaseHeightOffset = 0.5
jointTopRadius = 7.7 / 2
jointTopHeight = 10.0
jointTopThickness = 1.5
jointTopSpaceLength = 1.4
jointTopStopperWidth = 2.65
jointTopStopperHeight = 2.0
jointTopStopperLength = 1.0

pts = [
    (ringWidth/2, 0),
    (ringWidth/2, ringHeight),
    (ringWidth/2 - ringTopWidth, ringHeight),
    (-ringWidth/2, ringHeight - ringTopSpaceHeight),
    (-ringWidth/2, ringBottomSpaceHeight),
    (-ringWidth/2 + ringThickness, ringBottomSpaceHeight),
    (-ringWidth/2 + ringThickness, ringHeight - ringTopSpaceHeight - 0.5),
    # (ringWidth/2 - ringTopWidth + 0.5, ringHeight - ringThickness),
    (ringWidth/2 - ringThickness, ringHeight - ringThickness),
    (ringWidth/2 - ringThickness, 0),
]
supporterWidth = ringWidth - ringThickness
ringPoints = [
    (supporterWidth/2, ringBottomSpaceHeight),
    (supporterWidth/2, ringHeight - ringThickness/2),
    (ringWidth/2 - ringTopWidth + ringThickness/2,
     ringHeight - ringThickness/2),
    (- supporterWidth/2,
     ringHeight - ringThickness/2 - ringTopSpaceHeight),
    (- supporterWidth/2, ringBottomSpaceHeight)]
ringSupporter = cq.Workplane("XZ").moveTo(*ringPoints[0])\
    .polyline(ringPoints[1:]).close().extrude(ringSupporterThickness)\
    .translate((ringRadius, ringSupporterThickness/2, 0))
ringLine = cq.Workplane("XY")\
    .threePointArc((-ringRadius, ringRadius), (-ringRadius * 2, 0))
ring = cq.Workplane("XZ").moveTo(*pts[0]).polyline(pts[1:]).close()\
    .sweep(ringLine)\
    .translate((ringRadius, 0, 0))

holderFook = cq.Workplane("YZ").circle(holderFookRadius)\
    .extrude(-holderFookHeight)
holderStopper = cq.Workplane("YZ")\
    .box(holderStopperLength * 2, holderStopperWidth, holderStopperHeight)\
    .translate((-holderStopperHeight/2, -holderFookRadius, 0))
holder = cq.Workplane("YZ").circle(holderBaseRadius).extrude(holderBaseHeight)\
    .union(holderFook).union(holderStopper)

holderXOffset = ringRadius - (holderBaseHeight / 2) - 0.1
holderZOffset = holderBaseRadius - 0.5
holderRight = holder.translate((holderXOffset, 0, holderZOffset))
holderLeft = holder.mirror("YZ").translate((-holderXOffset, 0, holderZOffset))

stopperYOffset = jointTopStopperHeight / 2
stopperZOffset = -jointTopRadius
jointTopStopper = cq.Workplane("XZ")\
    .box(jointTopStopperWidth,
         jointTopStopperLength * 2,
         jointTopStopperHeight)
jointTopSpace = cq.Workplane("XZ")\
    .box(jointTopRadius * 2, jointTopSpaceLength, jointTopHeight * 2)
jointTop = cq.Workplane("XZ").circle(jointTopRadius).extrude(-jointTopHeight)\
    .faces(">Y").workplane().hole((jointTopRadius - jointTopThickness) * 2)\
    .cut(jointTopSpace)\
    .union(jointTopStopper.translate((0, stopperYOffset, stopperZOffset)))\
    .union(jointTopStopper.translate((0,
                                      jointTopHeight - stopperYOffset,
                                      stopperZOffset)))
jointCutPoints = [
    (-jointBaseRadius, 0),
    (- ringHeight/2, - jointBaseHeightOffset - jointBaseHeight),
    (- jointBaseRadius, - jointBaseHeightOffset - jointBaseHeight)]
jointCut = cq.Workplane("ZY").moveTo(*jointCutPoints[0])\
    .polyline(jointCutPoints[1:]).close().extrude(jointBaseRadius*2)\
    .translate((jointBaseRadius, 0, 0))
jointBase = cq.Workplane("XZ").circle(jointBaseRadius)\
    .extrude(jointBaseHeight + jointBaseHeightOffset)
# show(jointCut)
# show(jointBase)
joint = jointBase\
    .union(jointTop)\
    .cut(jointCut)\
    .translate((0, ringRadius + ringWidth/2 + jointBaseHeight, ringHeight/2))\
    .rotate((0, 0, 0), (0, 0, 1), 13)

ring = ring\
   .union(holderRight, clean=False)\
   .union(holderLeft)\
   .union(joint)

for i in range(0, ringSupporterNumber):
    ring = ring.union(ringSupporter.rotate((0, 0, 0), (0, 0, 1),
                                           180 * i / ringSupporterNumber))

show(ring)
# show_object(ring)
