import ReactDOM from "react-dom";
import React, { PureComponent } from "react";
import ReactCrop from "react-image-crop";
import "react-image-crop/dist/ReactCrop.css";

import "./App.css";
window.out = "out"
class App extends PureComponent {
  state = {
    src: null,
    crop: {
      unit: "%",
      width: 30,
      //aspect: 16 / 9
    },
    options: ["big customers", "small customers"],
    allCategories:[["Date", "Time", "Business", "Is Roee king? Of course"],["Date", "Times"]],
    categories: ["Date", "Time", "Business", "Is Roee king? Of course"]
  };

  onSelectFile = e => {
    if (e.target.files && e.target.files.length > 0) {
      const reader = new FileReader();
      reader.addEventListener("load", () =>
        this.setState({ src: reader.result })
      );
      reader.readAsDataURL(e.target.files[0]);
    }
  };

  // If you setState the crop in here you should return false.
  onImageLoaded = image => {
    this.imageRef = image;
  };

  onCropComplete = crop => {
    this.makeClientCrop(crop);
  };

  onCropChange = (crop, percentCrop) => {
    // You could also use percentCrop:
    // this.setState({ crop: percentCrop });
    this.setState({ crop });
  };

  async makeClientCrop(crop) {
    if (this.imageRef && crop.width && crop.height) {
      const croppedImageUrl = await this.getCroppedImg(
        this.imageRef,
        crop,
        "newFile.jpeg"
      );
      this.setState({ croppedImageUrl });
      this.requestParse(croppedImageUrl);
    }
  }

  async requestParse(croppedImageUrl){
    var blob = await fetch(croppedImageUrl).then(r => r.blob());
    var reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = function() {
        var base64audio = reader.result;
        //fetch('http://172.20.1.130:5000/upload', {
        fetch('http://192.168.1.15:5000/upload', {
    // content-type header should not be specified!
            method: 'POST',
            body: base64audio,
        })
        .then(response => response.text())
        .then(success => {
            console.log(success)
            window.out = success
        })
        .catch(error => {console.log(error);
            window.out = error
            alert("changed");
        });
    }
      //xhr.send(JSON.stringify({'test':'test2'}))
  }

  getCroppedImg(image, crop, fileName) {
    const canvas = document.createElement("canvas");
    const scaleX = image.naturalWidth / image.width;
    const scaleY = image.naturalHeight / image.height;
    canvas.width = crop.width;
    canvas.height = crop.height;
    const ctx = canvas.getContext("2d");

    ctx.drawImage(
      image,
      crop.x * scaleX,
      crop.y * scaleY,
      crop.width * scaleX,
      crop.height * scaleY,
      0,
      0,
      crop.width,
      crop.height
    );

    return new Promise((resolve, reject) => {
      canvas.toBlob(blob => {
        if (!blob) {
          //reject(new Error('Canvas is empty'));
          console.error("Canvas is empty");
          return;
        }
        blob.name = fileName;
        window.URL.revokeObjectURL(this.fileUrl);
        this.fileUrl = window.URL.createObjectURL(blob);
        resolve(this.fileUrl);
      }, "image/jpeg");
    });
  }

  putValue = () => {
    document.getElementById("category0").value = "3"
    window.out = "wow"
  }

  onClickPutValue = (id, value) =>{
    document.getElementById(id).value = value;
  }

  uploadVisible = () =>{
    document.getElementById("upload").style.visibility = "visible";
  }

  uploadInvisible = () =>{
    document.getElementById("upload").style.visibility = "hidden";
  }

  onChangeOption = () =>{
    ////works good
    var sel = document.getElementById("tableSelect");
    var text= sel.selectedIndex;
    //document.getElementById("category0").value = "10";
    this.setState({categories: this.state.allCategories[text]})
  }

  render() {
    const { crop, croppedImageUrl, src } = this.state;

    return (
      <div className="App">
        <ul className="NavigationBar">
          <li><a href="#upload" onClick={this.uploadVisible}>Upload</a></li>
          <li><a href="#home" onClick={this.uploadInvisible}>Home</a></li>
          <li><a href="#contact" onClick={this.uploadInvisible}>Contact</a></li>
          <li><a href="#about" onClick={this.uploadInvisible}>About</a></li>
        </ul>
        <div id="upload">
          <input type="file" onChange={this.onSelectFile} />
          <br/>
          <div class="Categories"  id="categories">
            <Selection options={this.state.options} onChange={this.onChangeOption} />
            <br/> <br/>
            {/* <CategoryList categories={this.state.categories} /> */}
            <CategoryList categories={this.state.categories} onClick={(id, value) => this.onClickPutValue(id, value)} />
            <input type="submit" value="Save" />
          </div>
          <button onClick={() => this.putValue()}>wow</button> <br/>
          {src && (
            <ReactCrop
                src={src}
                crop={crop}
                onImageLoaded={this.onImageLoaded}
                onComplete= {this.onCropComplete}
                onChange={this.onCropChange}
            />
          )}
          {croppedImageUrl && (
            <img alt="Crop" style={{ maxWidth: "100%" }} src={croppedImageUrl} />
          )}
        </div>
      </div>
    );
  }
}

function putValue(id, value){
    document.getElementById(id).value = value;
}

function CategoryList(props){
    const categories = props.categories;
    const listItems = categories.map((category, index) =>
        <div>
            {/* <button onClick={() => putValue("category" + index, window.out)}>{category}</button> */}
            <button onClick={() => props.onClick("category" + index, window.out)}>{category}</button>
            <br/>
            <input type="text" placeholder="Insert Here" id={"category"+index.toString()} />
            <br/>
            <br/>
        </div>
    );
    return(
        <form>
            <u1>{listItems}</u1>
        </form>
    );
}

function Selection(props){
    const options = props.options
    const listOptions = options.map((option) =>
        <option value={option}>{option}</option>
    );
    return(
        ////onChange here works
        //<select onChange={() => putValue("category0", window.out)}>{listOptions}</select>
        <select id="tableSelect" onChange={props.onChange}>{listOptions}</select> //good example of using props to define something inside the app class even though this function is outside
    );
}

//const categories = ["Date", "Time", "Business", "Is Roee king? Of course"];
//const options = ["big customers", "small customers"]
ReactDOM.render(<App />, document.getElementById("root"));