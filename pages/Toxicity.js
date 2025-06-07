const bandrectMEnter = (e) => {
  let bandrect = e.target
  let paths = bandrect.__data__.paths
  paths.forEach(
    (path) => {
      path.style.fill='rgba(225, 185, 0, 0.6)'
    }
  )
}

const bandrectMLeave = (e) => {
  let bandrect = e.target
  let paths = bandrect.__data__.paths
  paths.forEach(
    (path) => {
      path.style.fill='rgb(150, 150, 150)'
    }
  )
}

window.addEventListener('load', function() {
  //let dimensions = window.parent.document.querySelectorAll('g.dimension')
  //dimensions.forEach(
  //  category => console.log(category.__data__['model']['dimensionLabel'])
  //)

  const callback = (mutationList, observer) => {
    observer.disconnect()
    //console.log('bing!')
    let dimensions = window.parent.document.querySelectorAll('g.dimension')

    // Recolor each dimension to be a different color
    dimensions.forEach(
      (dimension) => {
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

    // Ensure labels are towards the "inside" of the chart
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

    // ensure paths are properly highlighted when necessary
    
    // create function to find paths associated with a bandrect
    const paths = Array.from(window.parent.document.querySelectorAll('path.path'))
    const getCatPaths = (bandrect, paths) => {
      let dimInd = bandrect.__data__.categoryViewModel.model.dimensionInd
      let catInd = bandrect.__data__.categoryViewModel.model.categoryInd

      //console.log(dimInd)
      //console.log(catInd)
      //console.log(paths)

      let cat_paths = paths.filter( 
        (path) => {
          return path.__data__.model.categoryInds[dimInd] == catInd
        }
      )
      //console.log(cat_paths)
      return cat_paths
    }

    // for each bandrect
    const bandrects = window.parent.document.querySelectorAll('rect.bandrect')
    bandrects.forEach( 
      (bandrect) => {

        // set its associated paths
        let bandpaths = getCatPaths(bandrect, paths)
        bandrect.__data__.paths = bandpaths

        // set callback functions for mouseEnter/mouseLeave
        bandrect.removeEventListener("mouseenter", bandrectMEnter)
        bandrect.removeEventListener("mouseleave", bandrectMLeave)
        bandrect.addEventListener("mouseenter", bandrectMEnter)
        bandrect.addEventListener("mouseleave", bandrectMLeave)
      }
    )

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

