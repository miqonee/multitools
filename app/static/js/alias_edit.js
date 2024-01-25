$(function() {
    $("div[data-toggle=fieldset]").each(function() {
        var $this = $(this);

        //Add new entry
        $this.find("button[data-toggle=fieldset-add-row]").click(function() {
            var target = $($(this).data("target"));
            var fs_id = target.attr("id");
            console.log(fs_id);
            var fs_type = fs_id.replace(/(.*)-fieldset/m, '$1');
            if (target.find("[data-toggle=fieldset-entry]").length>0) {
                var oldrow = target.find("[data-toggle=fieldset-entry]:last");
                var row = oldrow.clone(true, true);
                var elem_id = row.find(":input")[0].id;
                var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})/m, '$1')) + 1;
                row.attr('data-id', elem_num);
                row.find(":input").each(function() {
                    console.log(this);
                    var id = $(this).attr('id').replace('-' + (elem_num - 1), '-' + (elem_num));
                    $(this).attr('name', id).attr('id', id).val('');
                });
                row.show();
                oldrow.after(row);
            } else {
                target.append(
                    '<div data-toggle="fieldset-entry"' +
                        'class="input-append" style="display: block;">' +
                        '<input id="' + fs_type + '-0" name="' + fs_type + '-0"' +
                        ' value="" type="text">' +
                        '<button type="button" data-toggle="fieldset-remove-row"' +
                                'class="btn btn-danger" id="' + fs_type + '-0-remove">' +
                            '<i class="icon-minus"></i>' +
                        '</button>' +
                    '</div>')
            }
        }); //End add new entry

        //Remove row
        $this.find("button[data-toggle=fieldset-remove-row]").click(function() {
            if($this.find("[data-toggle=fieldset-entry]").length > 1) {
                var thisRow = $(this).closest("[data-toggle=fieldset-entry]");
                thisRow.remove();
            }
        }); //End remove row
    });
});
