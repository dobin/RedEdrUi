
    // Function to display events in Tab 1
    function displayEvents(events) {
        const eventContainer = document.getElementById('eventContainer');
        eventContainer.innerHTML = ''; // Clear previous content

        events.forEach(event => {
            const eventDiv = document.createElement('div');
            eventDiv.classList.add('event');

            let eventTitle = '';
            let eventHeader = '';
            let eventDetails = '';
            let eventCallstack = '';
            for (const [key, value] of Object.entries(event)) {
                // header
                if (key === 'type' || key === 'time' || key === 'pid' || key === 'tid' || key === 'krn_pid') {
                    eventHeader += `<span class="highlight_a">${key}:${value}</span>&nbsp`;
                } else if (key === 'func' || key === 'callback') {
                    eventTitle += `<span class="highlight_b"><b>${value}</b></span>&nbsp;&nbsp;`;

                // callstack
                } else if (key == 'callstack') { 
                    eventCallstack = '<span class="highlight_d">callstack:<br>' + JSON.stringify(value, null, 0) + "</span>";

                // important
                } else if (key === 'addr') {
                    eventDetails += `<b>${key}:${value}</b>&nbsp;&nbsp;`;
                } else if (key === 'protect') {
                    eventDetails += `<b>${key}:${value}</b>&nbsp;&nbsp;`;
                } else if (key === 'handle' && value != "FFFFFFFFFFFFFFFF") {
                    eventDetails += `<b>${key}:${value}</b>&nbsp;&nbsp;`;

                // rest
                } else {
                    eventDetails += `<span class="highlight_c">${key}:${value}</span>&nbsp;&nbsp;`;
                }
            }

            eventDiv.innerHTML = eventTitle + eventHeader + "<br>" + eventDetails + "<br>" + eventCallstack;
            eventContainer.appendChild(eventDiv);
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