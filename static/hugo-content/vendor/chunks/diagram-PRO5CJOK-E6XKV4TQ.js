import{a as E}from"./chunk-BZT6B5BA.js";import{a as F}from"./chunk-2N2FJ4OO.js";import"./chunk-NR3M2DWL.js";import"./chunk-X7AKENML.js";import"./chunk-CNXLXHHW.js";import"./chunk-5IEH6YRQ.js";import"./chunk-Z3BKX3T2.js";import"./chunk-HNVOIX6V.js";import"./chunk-GJLSBYZN.js";import"./chunk-WL7KYHKP.js";import"./chunk-TKRWIM2Z.js";import"./chunk-G4CVEYLA.js";import"./chunk-TQZXL4RJ.js";import"./chunk-RDWW76F7.js";import"./chunk-DRA4GI4L.js";import"./chunk-67UU673J.js";import"./chunk-OUM5NBOO.js";import"./chunk-7L5QQVB6.js";import{a as z}from"./chunk-IJ5QOXJV.js";import{o as w}from"./chunk-LNA7AKSF.js";import"./chunk-DUGKBEOY.js";import{O as y,T as $,U as B,V as C,W as S,X as D,Y as T,Z as P,j as v,t as x}from"./chunk-YI42TXK3.js";import{b as u}from"./chunk-OT2WJOTX.js";import{a as g}from"./chunk-HAKEUQOV.js";import"./chunk-IHRIUEAN.js";var L=v.packet,b,A=(b=class{constructor(){this.packet=[],this.setAccTitle=B,this.getAccTitle=C,this.setDiagramTitle=T,this.getDiagramTitle=P,this.getAccDescription=D,this.setAccDescription=S}getConfig(){let t=w({...L,...x().packet});return t.showBits&&(t.paddingY+=10),t}getPacket(){return this.packet}pushWord(t){t.length>0&&this.packet.push(t)}clear(){$(),this.packet=[]}},g(b,"PacketDB"),b),M=1e4,Y=g((e,t)=>{E(e,t);let a=-1,o=[],n=1,{bitsPerRow:l}=t.getConfig();for(let{start:r,end:s,bits:p,label:c}of e.blocks){if(r!==void 0&&s!==void 0&&s<r)throw new Error(`Packet block ${r} - ${s} is invalid. End must be greater than start.`);if(r??(r=a+1),r!==a+1)throw new Error(`Packet block ${r} - ${s??r} is not contiguous. It should start from ${a+1}.`);if(p===0)throw new Error(`Packet block ${r} is invalid. Cannot have a zero bit field.`);for(s??(s=r+(p??1)-1),p??(p=s-r+1),a=s,u.debug(`Packet block ${r} - ${a} with label ${c}`);o.length<=l+1&&t.getPacket().length<M;){let[d,i]=I({start:r,end:s,bits:p,label:c},n,l);if(o.push(d),d.end+1===n*l&&(t.pushWord(o),o=[],n++),!i)break;({start:r,end:s,bits:p,label:c}=i)}}t.pushWord(o)},"populate"),I=g((e,t,a)=>{if(e.start===void 0)throw new Error("start should have been set during first phase");if(e.end===void 0)throw new Error("end should have been set during first phase");if(e.start>e.end)throw new Error(`Block start ${e.start} is greater than block end ${e.end}.`);if(e.end+1<=t*a)return[e,void 0];let o=t*a-1,n=t*a;return[{start:e.start,end:o,label:e.label,bits:o-e.start},{start:n,end:e.end,label:e.label,bits:e.end-n}]},"getNextFittingBlock"),W={parser:{yy:void 0},parse:g(async e=>{let t=await F("packet",e),a=W.parser?.yy;if(!(a instanceof A))throw new Error("parser.parser?.yy was not a PacketDB. This is due to a bug within Mermaid, please report this issue at https://github.com/mermaid-js/mermaid/issues.");u.debug(t),Y(t,a)},"parse")},O=g((e,t,a,o)=>{let n=o.db,l=n.getConfig(),{rowHeight:r,paddingY:s,bitWidth:p,bitsPerRow:c}=l,d=n.getPacket(),i=n.getDiagramTitle(),h=r+s,m=h*(d.length+1)-(i?0:r),f=p*c+2,k=z(t);k.attr("viewBox",`0 0 ${f} ${m}`),y(k,m,f,l.useMaxWidth);for(let[_,N]of d.entries())j(k,N,_,l);k.append("text").text(i).attr("x",f/2).attr("y",m-h/2).attr("dominant-baseline","middle").attr("text-anchor","middle").attr("class","packetTitle")},"draw"),j=g((e,t,a,{rowHeight:o,paddingX:n,paddingY:l,bitWidth:r,bitsPerRow:s,showBits:p})=>{let c=e.append("g"),d=a*(o+l)+l;for(let i of t){let h=i.start%s*r+1,m=(i.end-i.start+1)*r-n;if(c.append("rect").attr("x",h).attr("y",d).attr("width",m).attr("height",o).attr("class","packetBlock"),c.append("text").attr("x",h+m/2).attr("y",d+o/2).attr("class","packetLabel").attr("dominant-baseline","middle").attr("text-anchor","middle").text(i.label),!p)continue;let f=i.end===i.start,k=d-2;c.append("text").attr("x",h+(f?m/2:0)).attr("y",k).attr("class","packetByte start").attr("dominant-baseline","auto").attr("text-anchor",f?"middle":"start").text(i.start),f||c.append("text").attr("x",h+m).attr("y",k).attr("class","packetByte end").attr("dominant-baseline","auto").attr("text-anchor","end").text(i.end)}},"drawWord"),G={draw:O},H={byteFontSize:"10px",startByteColor:"black",endByteColor:"black",labelColor:"black",labelFontSize:"12px",titleColor:"black",titleFontSize:"14px",blockStrokeColor:"black",blockStrokeWidth:"1",blockFillColor:"#efefef"},K=g(({packet:e}={})=>{let t=w(H,e);return`
	.packetByte {
		font-size: ${t.byteFontSize};
	}
	.packetByte.start {
		fill: ${t.startByteColor};
	}
	.packetByte.end {
		fill: ${t.endByteColor};
	}
	.packetLabel {
		fill: ${t.labelColor};
		font-size: ${t.labelFontSize};
	}
	.packetTitle {
		fill: ${t.titleColor};
		font-size: ${t.titleFontSize};
	}
	.packetBlock {
		stroke: ${t.blockStrokeColor};
		stroke-width: ${t.blockStrokeWidth};
		fill: ${t.blockFillColor};
	}
	`},"styles"),kt={parser:W,get db(){return new A},renderer:G,styles:K};export{kt as diagram};
