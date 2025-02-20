document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('dataset-modal');
    const modalContent = document.getElementById('dataset-details');
    const closeBtn = document.querySelector('.close');

    // 데이터셋 상세 보기 버튼 이벤트
    document.querySelectorAll('.view-details-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const card = btn.closest('.dataset-card');
            const type = card.dataset.type;
            const name = card.dataset.name;

            try {
                const response = await fetch(`/dataset/${type}/${name}`);
                const data = await response.json();
                
                displayDatasetDetails(data);
                modal.style.display = 'block';
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });

    // 모달 닫기
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    function displayDatasetDetails(data) {
        // 데이터셋 상세 정보 표시 로직
        modalContent.innerHTML = `
            <h2>${data.name}</h2>
            <div class="dataset-details">
                <!-- 상세 정보 표시 -->
            </div>
        `;
    }
}); 