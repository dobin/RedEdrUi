
    // Function to display events in Tab 1
    function displayEvents(events) {
        const eventContainer = document.getElementById('eventContainer');
        eventContainer.innerHTML = ''; // Clear previous content

        events.forEach(event => {
            const eventDiv = document.createElement('div');
            eventDiv.classList.add('event');

            let eventDetails = '';
            for (const [key, value] of Object.entries(event)) {
                let formattedKeyValue;

                if (key === 'type' || key === 'time' || key === 'pid' || key === 'tid' || key === 'krn_pid') {
                    formattedKeyValue = `<span class="highlight_a">${key}:`;
                } else if (key === 'func' || key === 'callback') {
                    formattedKeyValue = `<span class="highlight_b">${key}:`;
                } else if (key === 'addr') {
                    formattedKeyValue = `<span class="highlight_c">${key}:`;
                } else if (key === 'protect') {
                    formattedKeyValue = `<span class="highlight_d">${key}:`;
                } else {
                    formattedKeyValue = `<span>${key}:`;
                }

                if (key == 'callstack') { 
                    formattedKeyValue = "<br>" + formattedKeyValue + "<br>";
                    formattedKeyValue += JSON.stringify(value, null, 0) + "</span>";
                } else {
                    formattedKeyValue += `${value}</span>`;
                }

                eventDetails += `${formattedKeyValue}; `;
            }

            eventDiv.innerHTML = eventDetails; // Set the inner HTML to the details
            eventContainer.appendChild(eventDiv); // Add the event div to the container
        });
    }
    
    // Function to display events in Tab 1
    function displayDetections(detections) {
        const container = document.getElementById('detectionContainer');
        container.innerHTML = '';

        detections.forEach((detection, index) => {
            // Create a div for each detection
            const detectionDiv = document.createElement('div');
            detectionDiv.textContent = `${index}: ${detection}`;
            container.appendChild(detectionDiv);
        });
    }