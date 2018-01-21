﻿
function getData() {

    var deferredData = new jQuery.Deferred();

    $.ajax({
        type: "GET",
        url: "/ajax",
        dataType: "json",
        success: function (data) {
            deferredData.resolve(data);
        },
        complete: function (xhr, textStatus) {
            console.log("AJAX Request complete -> ", xhr, " -> ", textStatus);
        },
        error: function () {
            $("#myModal").modal();
            console.log("Error occur");
        }
    });

    return deferredData; // contains the passed data
};
// I used the Deferred structure below because I later added Deferred objects from other asynchronous functions to the `.when`

var dataDeferred = getData();
var DataLabels = [];
var DataArray = [];

function checkAjaxStatuses() {
    var pending = [];
    var successes = [];
    var errors = [];
    for (var i = 0; i < resp.propertiesList.length; i++) {
        if (resp.propertiesList[i].ajaxStatus === 'pending') {
            pending.push(resp.propertiesList[i]);
        }
        if (resp.propertiesList[i].ajaxStatus === 'success') {
            successes.push(resp.propertiesList[i]);
        }
        if (resp.propertiesList[i].ajaxStatus.indexOf('error') !== -1) {
            errors.push(resp.propertiesList[i]);
        }
    }

    console.log('ajax completed.');
    console.log(pending.length + ' pending.');
    console.log(successes.length + ' succeeded.');
    console.log(errors.length + ' failed.');
}

$.when(dataDeferred).done(function (data) {
    console.log("Okay");

    for (i = 0; i < data.nBlackPixelArrylst.length; i++) {
        var DataItem = (data.nBlackPixelArrylst[i] / data.nAllPixelArrylst[i]) * data.FrameSize;
        DataArray.push(DataItem);
        var LabelItem = "Image " + i;
        DataLabels.push(LabelItem);
    }
    $('#myTable').DataTable({
        ordering: true
    });
});