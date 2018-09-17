$(document).ready(function () {

    $(function () {
        if ($(".datetimepicker").length) {
            $(".datetimepicker").datetimepicker({
                format: 'd-m-Y',
                maxDate: 0,
                timepicker: false,
                inline: true,
                theme: "dark"
            });
        }
    });

    function prepare_buttons() {
        var conditionRow = $('.form-row:not(:last)');
        conditionRow.find('.btn.add-form-row')
            .removeClass('btn-success').addClass('btn-danger')
            .removeClass('add-form-row').addClass('remove-form-row')
            .html('<span class="glyphicon glyphicon-minus" aria-hidden="true">-</span>');
    }

    function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+)');
        var replacement = prefix + '-' + ndx;
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    function cloneMore(selector, prefix) {
        var newElement = $(selector).clone(true);
        var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
        newElement.find('input, textarea, select')
            .not(':input[type=button], :input[type=submit], :input[type=reset]').each(function () {
            $(this).val('');
            var name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        });
        total++;
        $('#id_' + prefix + '-TOTAL_FORMS').val(total);
        $(selector).after(newElement);
        prepare_buttons();
        return false;
    }

    function deleteForm(prefix, btn) {
        var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (total > 1) {
            btn.closest('.form-row').remove();
            var forms = $('.form-row');
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            for (var i = 0, formCount = forms.length; i < formCount; i++) {
                $(forms.get(i)).find(':input').each(function () {
                    updateElementIndex(this, prefix, i);
                });
            }
        }
        return false;
    }

    prepare_buttons();

    $(document).on('click', '.add-form-row', function (e) {
        e.preventDefault();
        cloneMore('.form-row:last', 'form');
        return false;
    });
    $(document).on('click', '.remove-form-row', function (e) {
        e.preventDefault();
        deleteForm('form', $(this));
        return false;
    });

});


