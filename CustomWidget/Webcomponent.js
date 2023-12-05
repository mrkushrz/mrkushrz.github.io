function UI5(changedProperties, that) {
    var that_ = that;

    var div = document.createElement('div');
    var widgetName = that._export_settings.name;
    div.slot = "content_" + widgetName;

    var restAPIURL = that._export_settings.restapiurl;
    console.log("restAPIURL: " + restAPIURL);

    if (that._firstConnectionUI5 === 0) {
        console.log("--First Time --");

        let div0 = document.createElement('div');
        div0.innerHTML = '<?xml version="1.0"?><script id="oView_' + widgetName + '" name="oView_' + widgetName + '" type="sapui5/xmlview"><mvc:View xmlns="sap.m" xmlns:mvc="sap.ui.core.mvc" xmlns:core="sap.ui.core" xmlns:l="sap.ui.layout" height="100%" controllerName="myView.Template"><l:VerticalLayout class="sapUiContentPadding" width="100%"><l:content><Input id="input"  placeholder="Enter partner number..." liveChange=""/></l:content><Button id="buttonId" class="sapUiSmallMarginBottom" text="Get Score" width="150px" press=".onButtonPress" /></l:VerticalLayout></mvc:View></script>';
        _shadowRoot.appendChild(div0);

        let div1 = document.createElement('div');
        div1.innerHTML = '<div id="ui5_content_' + widgetName + '" name="ui5_content_' + widgetName + '"><slot name="content_' + widgetName + '"></slot></div>';
        _shadowRoot.appendChild(div1);

        that_.appendChild(div);

        var mapcanvas_divstr = _shadowRoot.getElementById('oView_' + widgetName);

        Ar.push({
            'id': widgetName,
            'div': mapcanvas_divstr
        });
        console.log(Ar);
    }

    sap.ui.getCore().attachInit(function() {
        "use strict";

        sap.ui.define([
            "jquery.sap.global",
            "sap/ui/core/mvc/Controller",
            "sap/m/MessageToast",
            'sap/m/MessageBox'
        ], function(jQuery, Controller, MessageToast, MessageBox) {
            "use strict";

            return Controller.extend("myView.Template", {

                onButtonPress: function(oEvent) {
                    var startDate = oView.byId("startDateInput").getValue();
                    var endDate = oView.byId("endDateInput").getValue();
                    var commodity = oView.byId("commodityInput").getValue();
                    var type = oView.byId("typeInput").getValue();

                    $.ajax({
                        url: restAPIURL,
                        type: 'POST',
                        data: $.param({
                            "start_date": startDate,
                            "end_date": endDate,
                            "commodity": commodity,
                            "type": type
                        }),
                        contentType: 'application/x-www-form-urlencoded',
                        success: function(data) {
                            console.log(data);
                            // handle response
                        },
                        error: function(e) {
                            console.log("error: " + e);
                        }
                    });
                }
            });
        });

        console.log("widgetName:" + widgetName);
        var foundIndex = Ar.findIndex(x => x.id == widgetName);
        var divfinal = Ar[foundIndex].div;

        //### THE APP: place the XMLView somewhere into DOM ###
        var oView = sap.ui.xmlview({
            viewContent: jQuery(divfinal).html(),
        });

        oView.placeAt(div);

        if (that_._designMode) {
            oView.byId("buttonId").setEnabled(false);
            oView.byId("input").setEnabled(false);
        } else {
            oView.byId("buttonId").setEnabled(true);
            oView.byId("input").setEnabled(true);
        }
    });
}
