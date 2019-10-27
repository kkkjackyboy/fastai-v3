var el = x => document.getElementById(x);

function showPicker() {
  el("file-input").click();
}

function showPicked(input) {
  el("upload-label").innerHTML = input.files[0].name;
  var reader = new FileReader();
  reader.onload = function(e) {
    el("image-picked").src = e.target.result;
    el("image-picked").className = "";
    
    //el("image-picked2").src = e.target.result;
    //el("image-picked2").className = "";
  };
  reader.readAsDataURL(input.files[0]);
}

function showPicked2() {
  //el("upload-label").innerHTML = input.files[0].name;
  var uploadFiles = el("file-input").files;
  if (uploadFiles.length !== 1) alert("Please select a file to analyze!");

  el("analyze-button").innerHTML = "Analyzing...";
  
  var reader = new FileReader();
  reader.onload = function(e) {
    el("image-picked2").src = e.target.result;
    el("image-picked2").className = "";
    
    //el("image-picked2").src = e.target.result;
    //el("image-picked2").className = "";
  };
  reader.readAsDataURL(uploadFiles[0]);

}

function analyze() {
  var uploadFiles = el("file-input").files;
  if (uploadFiles.length !== 1) alert("Please select a file to analyze!");

  el("analyze-button").innerHTML = "Analyzing...";

  var xhr = new XMLHttpRequest();
  var loc = window.location;
  xhr.open("POST", `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`,
    true);
  xhr.onerror = function() {
    alert(xhr.responseText);
  };

  // ��json response��ʽ����server.py�С�analyze(request)�����͹������ı���Ϣ
  // �������Ʒ��������Խ���ͼ�����ݣ�ͼ�������Ƿ������PNG����ѹ������Ҫ��
  // �������ݴ�С��PNGѹ���ļ����бȽ�ȷ�ϣ�
  //xhr.responseType = 'document';
  xhr.onload = function(e) {
    if (this.readyState === 4) {
      //var response = JSON.parse(e.target.responseText);
      //el("result-label").innerHTML = `Result = ${response["result"]}`;
	  el("analyze-button").innerHTML = "...............";
	  el("image-picked").src = e.target.response;

    }
    el("analyze-button").innerHTML = "Analyze";
  };

  // ��xhr.open��server.py�С�analyze(request)�������󣬷���ͼ������
  var fileData = new FormData();
  fileData.append("file", uploadFiles[0]);
  xhr.send(fileData);
}
