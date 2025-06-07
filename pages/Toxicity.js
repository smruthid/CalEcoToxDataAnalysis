window.addEventListener('load', function() {
  //let dimensions = window.parent.document.querySelectorAll('g.dimension')
  //dimensions.forEach(
  //  category => console.log(category.__data__['model']['dimensionLabel'])
  //)

  const callback = (mutationList, observer) => {
    observer.disconnect()
    //console.log('bing!')
    let dimensions = window.parent.document.querySelectorAll('g.dimension')

    dimensions.forEach(
      (dimension) => {
        // Recolor each dimension to be a different color
        //console.log(dimension.__data__['model']['dimensionLabel'])
        //console.log(dimension)
        //console.log(bandrects)
        let bandrects = dimension.querySelectorAll('rect.bandrect')
        let color = '#000000'
        let label = dimension.__data__['model']['dimensionLabel']
        if (label == 'Animal Name') {
          color = 'cyan'
        } else if (label == 'Chemical') {
          color = 'salmon'
        } else if (label == 'Exposure Category') {
          color = 'green'
        } else if (label = 'Exposure Technique') {
          color = 'seagreen'
        }
        bandrects.forEach(
          rect => rect.style.fill=color
        )
      }
    )

    const dimsort = (dimA, dimB) => {
      return dimA.getBoundingClientRect().x - dimB.getBoundingClientRect().x
    }
    dimensions = Array.from(dimensions)
    dimensions.sort(dimsort)

    const setLabel = (dim, isLeft) => {
      let catlabels = dim.querySelectorAll('text.catlabel')

      let newX = -5
      let newAnc = 'end'

      if (!isLeft) {
        newX = 21
        newAnc = 'start'
      }
      
      catlabels.forEach(
        (label) => {
          label.setAttribute('x', newX) 
          label.setAttribute('text-anchor', newAnc)

          let tspans = label.querySelectorAll('tspan')
          tspans.forEach(
            (tspan) => {
              tspan.setAttribute('x', newX)
              tspan.setAttribute('text-anchor', newAnc)
            }
          )
        }
      )
    }

    for (const [i, dim] of dimensions.entries()) {
      if (i < 1) {
        setLabel(dim, false)
      } else {
        setLabel(dim, true)
      }
    }
    //dimensions.forEach(
    //  (dimension) => {
    //    setLabel(dimension, false)
    //  }
    //)

    observer.observe(targetchart, config)
  }
  const observer = new MutationObserver(callback)


  const targetchart = window.parent.document.querySelector('div.stMainBlockContainer')
  const config = {attributes: true, childList: true, subtree: true };

  observer.observe(targetchart, config)

})

//const callback = (mutationList, observer) => {
//  console.log('bing!')
//  let dimensions = window.parent.document.querySelectorAll('g.dimension')
//  dimensions.forEach(
//    category => console.log(category.__data__['model']['dimensionLabel'])
//  )
//}
//
//const observer = new MutationObserver(callback)
//
//const targetchart = window.parent.document.querySelector('div.stPlotlyChart')
//const config = {attributes: true, childList: true, subtree: true };
//
//observer.observe(targetchart, config)

