mode = 0
// 0 pick starter
// 1 pick class tree
// 2  o o o next class tree
jobs = [null,null,null,null]
tree = null 
index = 0
max_sp = [15,45,45,45]
spent_sp = [0,0,0,0]
skills = [[],[],[],[]]
tree_by_id = {'1001':"Warrior", '2001': 'Wizard', '3001':'Archer', '4001': 'Cleric', '5001': 'Scout'}

class_div = $("#classes")[0]
parseUrl()

function hideAll(){
  items = $('.jobs')
  for (k in items){
    items[k].hidden = true
  }
}

function makeUrl(){
  url = ""
  for (j=0; j<jobs.length; j++){
    o = jobs[j]
    if (o == null){
      break
    }
    url+= "{"+ o  + "}"
    for (s in skills[j]){
      k = skills[j][s].toString(16)
      url += k
    }
  }
  curUrl = window.location.href.split("?d=")[0]
  nextUrl = curUrl +"?d="+ url 
  window.history.replaceState({},'',nextUrl)  
}

function parseUrl(){
  jobs = [null,null,null,null]
  tree = null 
  index = 0
  max_sp = [15,45,45,45]
  spent_sp = [0,0,0,0]
  skills = [[],[],[],[]]
  curUrl = window.location.href 
  data = curUrl.split("?d=")[1]
  data = data.replaceAll("%7B", "{")
  data = data.replaceAll("%7D", "}")
  if (data){
    mode = 2
    if (data.indexOf("j")>-1){
      split_by_jobs = data.split('c')
    }
    else {      
      split_by_jobs = data.split('{')  
   }    
    for (var i= 1; i<split_by_jobs.length; i++){
      //picking jobs
      if (data.indexOf("j")>-1){
        k = split_by_jobs[i].split('j')
      }
   else{
 k = split_by_jobs[i].split('}')
}
      jobs[i-1] = k[0]
      job       = k[0]
      skill     = k[1]
      if (k[0] in tree_by_id)
        tree = tree_by_id[k[[0]]]
      pickJob(k[0], i-1)
      for (z = 0; z<skill.length;z++){
        //adding skills
        x = skill[z]
        skills[i-1].push( parseInt(x,16))
        addSkillPointN(z, job, parseInt(x,16))
        
      }
    }
  }
  if (index>=4){
    $("#next")[0].hidden=true
  }
}

function addSkillPointN(ids, job, n){
  job = job+""
  if (jobs.indexOf(job) == -1 )
    return 0
  
  index_job = jobs.indexOf(job)
  
  $("#lv-"+ids+"-"+job)[0].innerText = n

  dataset = $("#img-"+ids+"-"+job)[0].dataset
  
  spent_sp[index_job] += n 
  $("#spentPoint-"+job)[0].innerText = spent_sp[index_job]
  setDesc(ids,job, dataset, n)
}

function pickJob(ids, index_cur){
  
  element = $("#"+ids).clone(true)
  element.addClass('current')
  container = $("#class"+index)[0]

  for (a = index; a<4; a++){
    jobs[a] = null
    $("#class"+a).empty()
  }
  jobs[index] = ids 


  container = $("#class"+index)[0]
  container.appendChild(element[0])

  



  element = $('#skillsJob-'+ids).clone(true)

  element.addClass('skillsJobActivated')

  container = $("#skillbar" + index)[0]
  container.appendChild(element[0])
  element[0].hidden = false

  $("#skillbar" + index).find(".skill-icon").each(
    function(ind){
          this.src = this.dataset.src
        })
  $("#skillbar" + index).find(".skill-icon").addClass('activatedSkill')
  mode = 2
  index += 1
  showCurrent()  
  mover()
  if(index<4)
    $("#next")[0].hidden=false
  
}

function unpickJob(index_cur){
  for (a = index_cur; a<4; a++){
    jobs[a] = null
    skills[a] = []
    $("#class"+a).empty()
    $("#skillbar" + a).empty()
    spent_sp[a] = 0
  }
  index= index_cur
}

function showTree(){
  items = $('.'+tree)
  mode =1
  $("#next")[0].hidden=true
  for (k in items){
    if (jobs.indexOf(items[k].id + '')>-1){
      continue
    }
    items[k].hidden = false
  }
}

function showStarter(){
  items = $('.starter')
  mode = 0
  $("#next")[0].hidden=true
  for (k in items){
    if (jobs.indexOf(items[k].id + '')>-1){
      continue
    }
    items[k].hidden = false
  } 
}

function showCurrent(){
  hideAll()
   items = $('.current')
  for (k in items)
    items[k].hidden = false
}

function hideCurrent(){
   items = $('.current')
  for (k in items)
    items[k].hidden = true
}

function showNext(){
  cls_img = $("<img loading='lazy' class = 'icon-job rmv' id = 'next', src = '/static/icons/job_next.png' onclick = selectClass('next')> ")
  class_div.append(cls_img[0])
}

function selectClass(ids,starter, curTree){
  ids = ids+''
  if (mode == 0){
    // ask for class tree
    // ask for class tree icons
    tree = curTree

    hideAll()
    pickJob(ids, 0)
    makeUrl()
  }
  else if (mode ==1) {
    
    pickJob(ids, index)
    // addSkill(ids)
    mode = 2
    makeUrl()
  }
  else if (mode ==2){
    changed = jobs.indexOf(ids)
    if (changed == 0){
      unpickJob(changed)
      mode = 0
      showStarter()
      makeUrl()
    }
    else if (ids == 'next'){
      mode = 1
      hideCurrent()
      showTree()
      makeUrl()
    }
    else{
      unpickJob(changed)
      hideCurrent()
      showTree()
      makeUrl()
    }
  }
}

function addSkillPoint(ids, job, dataset){
  job = job+""
  if (jobs.indexOf(job) == -1 )
    return 0
  
  index_job = jobs.indexOf(job)
  sp =parseInt ($("#lv-"+ids+"-"+job)[0].innerText)
  // maxsp = parseInt ($("#maxlv-"+ids+"-"+job)[0].innerText)
  maxsp = parseInt(dataset.maxsp)

  if (sp == maxsp){
    sp = -1
    spent_sp[index_job] -= (maxsp +1 )
  }

  if (spent_sp[index_job] == max_sp[index_job] ){
    return 0
  }
  
  $("#lv-"+ids+"-"+job)[0].innerText = sp+1
  
  
  while (skills[index_job].length -1  < ids){
    skills[index_job].push(0)
  }
  skills[index_job][ids] = sp +1
  
  spent_sp[index_job] +=1 
  $("#spentPoint-"+job)[0].innerText = spent_sp[index_job]

  setDesc(ids,job, dataset, sp+1)

  makeUrl()



  return 1
}


function removeSkillPoint(ids, job, dataset){
  job = job+""
  if (jobs.indexOf(job) == -1 )
    return 0
  

  index_job = jobs.indexOf(job)
  sp =parseInt ($("#lv-"+ids+"-"+job)[0].innerText)
  // maxsp = parseInt ($("#maxlv-"+ids+"-"+job)[0].innerText)
  maxsp = parseInt(dataset.maxsp)
  if (sp ==0 && spent_sp[index_job] >= max_sp[index_job] ){
    return 0 
  }
  

  if (sp == 0 ){
    if (spent_sp[index_job] + (maxsp +1) > max_sp[index_job]){
      sp = max_sp[index_job] - spent_sp[index_job] +1
      spent_sp[index_job] = max_sp[index_job] +1
    }
    else{
      sp = maxsp+1
      spent_sp[index_job] += (maxsp +1)  
    }
  }
  
  $("#lv-"+ids+"-"+job)[0].innerText = sp-1
  
  
  while (skills[index_job].length -1  < ids){
    skills[index_job].push(0)
  }
  skills[index_job][ids] = sp-1
  
  spent_sp[index_job] -=1 
  $("#spentPoint-"+job)[0].innerText = spent_sp[index_job]
  setDesc(ids,job, dataset, sp-1)
  makeUrl()
  return 1
}





function setDesc(skill,job, dataset, skillLV){

  elementparent = $('.skillsJobActivated').find("#skill-"+skill+"-"+job)


  if (dataset.captionratio1 != "None"){
    datasrc = JSON.parse(dataset.captionratio1)
    element = elementparent.find('#CaptionRatio')
    for (i in element){
      element[i].innerText = datasrc[skillLV]
    }
    
  }

  if (dataset.captionratio2 != "None"){
    datasrc = JSON.parse(dataset.captionratio2)
    element = elementparent.find('#CaptionRatio2')
    for (i in element){
      element[i].innerText = datasrc[skillLV]
    }
  }

  if (dataset.captionratio3 != "None"){
    datasrc = JSON.parse(dataset.captionratio3)
    element = elementparent.find('#CaptionRatio3')
    for (i in element){
      element[i].innerText = datasrc[skillLV]
    }
  }

  if (dataset.captiontime != "None"){
    datasrc = JSON.parse(dataset.captiontime)
    element = elementparent.find('#CaptionTime')
    for (i in element){
      element[i].innerText = datasrc[skillLV]
    }
  }

  if (dataset.skillsr != "None"){
    datasrc = JSON.parse(dataset.skillsr)
    element = elementparent.find('#SkillSR')
    for (i in element){
      element[i].innerText = datasrc[skillLV]
    }
  }

  if (dataset.spenditemcount != "None"){
    datasrc = JSON.parse(dataset.spenditemcount)
    element = elementparent.find('#SpendItemCount')
    for (i in element){
      element[i].innerText = datasrc[skillLV]
    }
  }

  if (dataset.spendsp != "None"){
    datasrc = JSON.parse(dataset.spendsp)
    element = elementparent.find('#SpendSP')
    for (i in element){
      element[i].innerText = datasrc[skillLV]
    }
  }

  if (dataset.spendpoison != "None"){
    datasrc = JSON.parse(dataset.spendpoison)
    element = elementparent.find('#SpendPoison')
    for (i in element){
      element[i].innerText = datasrc[skillLV]
    }
  }

  if (dataset.sfr != "None"){

    datasrc = JSON.parse(dataset.sfr)
    element = elementparent.find('#SkillFactor')
    for (i in element){
      element[i].innerText = datasrc[skillLV]
    }
  }

  if (dataset.cooldown_lv != "None"){

    datasrc = JSON.parse(dataset.cooldown_lv)
    element = elementparent.find('#cd')
    for (i in element){
      element[i].innerText = datasrc[skillLV] / 1000
    }
  }

}


function destroyDesc(desc) {
  // console.log(desc)
  if (desc.dataset.x == "r")
    desc.style.left = parseInt(desc.style.left.replace("p","").replace("x",''))+5 + "px"
  else
    desc.style.left = parseInt(desc.style.left.replace("p","").replace("x",''))-5 + "px"
  desca = desc
  return 1
}

function mover(){
   var tooltip = document.querySelectorAll('.skl-dsc');
    var tooltip_attr = document.querySelectorAll('.skl-dsc2');

    document.addEventListener('mousemove', fn, false);
    // document.addEventListener('click', fn, false);

    function fn(e) {
        windowHeight = $(window).height()
        windowWidth = $(window).width()
        for (var i=tooltip.length; i--;) {
            elementHeight = tooltip[i].offsetHeight
            elementWidth = tooltip[i].offsetWidth
            if (elementHeight==0){
              continue
            }
            if (e.pageX +50 + elementWidth > windowWidth){
              tooltip[i].style.left = e.pageX-5 - elementWidth+ 'px';
              tooltip[i].dataset.x = "l"
            }
            else{
              tooltip[i].style.left = e.pageX+50 + 'px';  
              tooltip[i].dataset.x = "r"
            }

            
            if (e.pageY+5 + elementHeight  > windowHeight+ $ (window).scrollTop ()){
              tooltip[i].style.top = windowHeight - elementHeight + $ (window).scrollTop ()+ 'px';
            }
            else{
              tooltip[i].style.top = e.pageY+5 + 'px';  
            }
            
        }
        
    }
   //return 1
}

$( document ).ready(function() {
   mover()
});
