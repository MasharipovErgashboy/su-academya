(function () {
    // Jazzmin/Django jQuery might be in different places
    const $ = (typeof django !== 'undefined' && django.jQuery) || (typeof jQuery !== 'undefined' && jQuery) || (typeof $ !== 'undefined' && $);

    if (!$) {
        console.error('jQuery not found for admin_audio.js');
        return;
    }

    $(document).ready(function () {
        console.log('admin_audio.js: System initialized');

        function addGenerateButton(container, nationality, wordId = null) {
            // Jazzmin/Bootstrap structure might differ, so we look for both standard and common Jazzmin patterns
            const jpField = container.find('.field-jp_word input, #id_jp_word');
            const uzField = container.find('.field-uz_word input, #id_uz_word');
            const audioInput = container.find('.field-audio input');

            let targetField = null;
            let lang = '';

            if (nationality === 'uz') {
                targetField = jpField;
                lang = 'ja';
            } else if (nationality === 'ja') {
                targetField = uzField;
                lang = 'uz';
            }

            if (targetField && targetField.length) {
                targetField.each(function () {
                    const field = $(this);
                    // Check if already has a button
                    if (!field.parent().find('.btn-generate-audio').length) {
                        const btn = $('<button type="button" class="button btn-generate-audio" style="margin-left: 10px; background: #264b5d; color: white; border: none; padding: 5px 12px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 11px;">🔊 GENERATE AUDIO</button>');
                        field.after(btn);

                        btn.on('click', function () {
                            const text = field.val();
                            if (!text) {
                                alert('Iltimos, avval so\'zni kiriting!');
                                return;
                            }

                            const originalText = btn.text();
                            btn.text('⌛ YARATILMOQDA...').prop('disabled', true).css('opacity', '0.7');

                            $.ajax({
                                url: '/admin/vocabulary/vocabularyword/generate-audio/',
                                method: 'POST',
                                data: {
                                    text: text,
                                    lang: lang,
                                    word_id: wordId,
                                    csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
                                },
                                success: function (data) {
                                    if (data.success) {
                                        // Update hidden field for save
                                        if (audioInput.length) {
                                            audioInput.val(data.rel_path);
                                        }

                                        // Show feedback
                                        const feedbackId = 'audio-feedback-' + (wordId || Math.random().toString(36).substr(2, 9));
                                        let feedback = $('#' + feedbackId);
                                        if (!feedback.length) {
                                            feedback = $(`<span id="${feedbackId}" style="margin-left:15px; font-weight:bold; color:#28a745;"></span>`);
                                            btn.after(feedback);
                                        }
                                        feedback.html(`✅ <a href="${data.url}" target="_blank" style="color:#28a745; text-decoration:underline;">Eshitish</a>`);
                                    } else {
                                        alert('Xatolik: ' + data.error);
                                    }
                                },
                                error: function () {
                                    alert('Tarmoq xatosi yuz berdi');
                                },
                                complete: function () {
                                    btn.text(originalText).prop('disabled', false).css('opacity', '1');
                                }
                            });
                        });
                    }
                });
            }
        }

        function checkAndAttach() {
            // Case 1: Topic Admin (Inlines)
            const topicNationality = $('#id_nationality').val();
            if (topicNationality) {
                $('.inline-related').each(function () {
                    const row = $(this);
                    // Finding the ID in inline rows
                    const wordId = row.find('.field-id input').val() || null;
                    addGenerateButton(row, topicNationality, wordId);
                });
            }

            // Case 2: Word Admin (Standalone)
            const topicSelect = $('#id_topic');
            if (topicSelect.length && topicSelect.val()) {
                const topicText = topicSelect.find('option:selected').text();
                const nationality = topicText.includes('[uz]') ? 'uz' : (topicText.includes('[ja]') ? 'ja' : null);
                if (nationality) {
                    const pathParts = window.location.pathname.split('/');
                    const wordId = pathParts[pathParts.length - 3];
                    const id = isNaN(wordId) ? null : wordId;
                    addGenerateButton($('.change-form'), nationality, id);
                }
            }
        }

        // Initial run
        checkAndAttach();

        // Jazzmin specific: handle tab changes
        $(document).on('shown.bs.tab', 'a[data-toggle="tab"]', function (e) {
            checkAndAttach();
        });

        // django-admin specific: formset additions
        $(document).on('formset:added', function (event, $row, formsetName) {
            checkAndAttach();
        });

        // Periodic check as a fallback for dynamic elements
        const interval = setInterval(checkAndAttach, 2000);

        // Stop interval after 30 seconds to save resources
        setTimeout(() => clearInterval(interval), 30000);

        // Listen for nationality change
        $(document).on('change', '#id_nationality', function () {
            // Remove old buttons first if nationality changed
            $('.btn-generate-audio').remove();
            checkAndAttach();
        });

        // Listen for topic change in standalone word admin
        $(document).on('change', '#id_topic', checkAndAttach);
    });
})();
