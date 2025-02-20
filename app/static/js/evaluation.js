document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const resultsSection = document.querySelector('.results-section');
    
    // 드래그 앤 드롭 이벤트 처리
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', async (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        const file = e.dataTransfer.files[0];
        if (file && file.name.endsWith('.json')) {
            await handleFile(file);
        }
    });

    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (file) {
            await handleFile(file);
        }
    });

    async function handleFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/evaluation/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (data.status === 'success') {
                displayResults(data);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function displayResults(data) {
        resultsSection.style.display = 'block';
        
        // 차트 생성
        const ctx = document.getElementById('cer-chart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.models,
                datasets: [{
                    label: 'CER',
                    data: data.cer_values,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // 테이블 데이터 표시
        const tbody = document.querySelector('#results-table tbody');
        tbody.innerHTML = ''; // 기존 데이터 초기화
        
        // 각 모델의 전사 결과를 테이블에 추가
        Object.entries(data.transcriptions).forEach(([model, results]) => {
            results.forEach(result => {
                const row = document.createElement('tr');
                
                // 오디오 파일 경로에서 파일명만 추출
                const audioName = result.audio_filepath.split('/').pop();
                
                row.innerHTML = `
                    <td>${audioName}</td>
                    <td>${result.sentence || '-'}</td>
                    <td>${result.pred_sentence}</td>
                    <td>${data.cer_metric[model].toFixed(4)}</td>
                `;
                
                tbody.appendChild(row);
            });
        });
    }
}); 