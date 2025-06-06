window.addEventListener('load', function() {
  //let dimensions = window.parent.document.querySelectorAll('g.dimension')
  //dimensions.forEach(
  //  category => console.log(category.__data__['model']['dimensionLabel'])
  //)

  const callback = (mutationList, observer) => {
    //console.log('bing!')
    let dimensions = window.parent.document.querySelectorAll('g.dimension')
    dimensions.forEach(
      (category) => {
        //console.log(category.__data__['model']['dimensionLabel'])
        //console.log(category)
        //console.log(bandrects)
        let bandrects = category.querySelectorAll('rect.bandrect')
        let color = '#000000'
        let label = category.__data__['model']['dimensionLabel']
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

