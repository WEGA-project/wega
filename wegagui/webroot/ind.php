<?php
echo "

<style>
.battery{
  position: relative;
  top: 10px;
  border: 4px solid;
  width: 50px;
  height: 150px;
  margin: auto;
    margin-bottom: 50px;
  content: '';
 }
.battery::after{
  content: '';
  background: black;
  position: absolute;
  width: 20px;
  height: 6px;
  top: -10px;
  left: 15px;
  position: top 164px;
 }

.low {
  background: linear-gradient(0deg, #ED1C24 ".$_GET['prcnt']."%, white 0%);
}
</style>

</head>
<body>
    <div class='battery low'></div>
    
</body>

";

?>