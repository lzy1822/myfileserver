readme.txt
1、部署到網絡。--ok
2、自動加載。--ok
    網絡版，能夠實現自動加載。
    在根目录中写入自定义的cor文件，并且在config.js中配置上cor的文件名于：corpora:[] 中，即可。
3、返回按鈕。--ok
    本頁面都是在一個頁面的react控件內實現的，沒有跳轉頁面。並沒有禁用。
4、禁用複製。--ok
    目前限制100字。
5、封面，研究下，如何存儲導入的cor文件。--ok
    同2.
6、表格轉化。

7、脚注。
    贤就在研究下，在下面的校注。

8、科判并列显示。
    研究 react 页面组织。
    DictView  右侧的字典页面。
    1-7目前已經基本能夠在右側顯示目錄了，也能調到左側。--ok
    
    另外還有一個是記錄選擇狀態。--OK
    還需要優化界面。滑竿。--ok
    左右寬窄。--ok

9、剪贴板问题。--ok
    限制500个字符。    


10、表格问题。--贤就

    homebar:{color:"white"}

    E("div",{style:styles.homebar},

11、去掉顶上的科判。去掉搜索中的标点。    


啟動函數：
	ReactDOM.render(E(MainScreen,opts), document.getElementById('root'))	


頂端菜單欄：
class HomeBar extends React.Component



const styles={
body:{overflowY:"auto",height:"96%",overflowX:"hidden"}
}

	,E("div",{style:styles.body,ref:this.getBodyRef.bind(this)}
				,E(bodyElement,props)
				,this.showFooter()
			)




-----------------------------
const krange=this.kRangeFromCursor(cm);
if (this.props.copyText) { //for excerpt copy
        evt.target.value=this.props.copyText(
            {cm:cm,value:evt.target.value,krange:krange,cor:this.cor,fields:this.props.fields});
        evt.target.select();
    }
}
   
    //if (this.props.copyText) { //for excerpt copy
//      if ( evt.target.value.length >100)
//      {
      //     evt.target.value=("仅能拷贝100个以内字符");
      //     console.log("仅能拷贝100个以内字符");
      //     //alert('提示','仅能拷贝100个以内字符');
      // }
      //else{
        evt.target.value=this.props.copyText(
          {cm:cm,value:evt.target.value,krange:krange,cor:this.cor,fields:this.props.fields});
      //}			
      
      
      if ( evt.target.value.length >100)
      {
          evt.target.value=("仅能拷贝100个以内字符");
          console.log("仅能拷贝100个以内字符");
          //alert('提示','仅能拷贝100个以内字符');
      }
      console.log(evt.target.value);
      console.log(evt.target.value.length);
      evt.target.select();
      //else{
		//}