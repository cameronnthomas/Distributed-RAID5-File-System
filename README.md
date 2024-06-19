# Distributed Unix-like File System with RAID5

## Overview
This repository hosts a distributed Unix-like file system designed to support multiple servers with RAID5 redundancy. The project aims to distribute data across servers to enhance fault tolerance, increase aggregate capacity, and optimize performance. This system is implemented using client/server architecture, providing robust functionality for file management, data storage, and retrieval.

## Key Features
- **RAID5 Redundancy**: Parity data is distributed across multiple servers, ensuring fault tolerance against the failure of a single server.
- **Client/Server Architecture**: Implements a layered approach with a client-side system that communicates with servers via XML-RPC for data storage and retrieval.
- **File System Operations**: Supports essential file system operations such as creating directories, reading and writing files, managing hard and symbolic links, and resolving file paths.
- **Concurrency Control**: Utilizes synchronization mechanisms like acquire and release to prevent race conditions and ensure data consistency in multi-client environments.
- **Fault Handling**: Implements error handling mechanisms to recover from server timeouts, disconnections, or data corruption scenarios during read and write operations.
- **Performance**: Demonstrates improved read and write performance compared to single server systems, particularly highlighted in RAID5 configurations.

## Components
- **Block Server**: Manages raw disk access and implements the block layer with Get() and Put() interfaces. Supports checksum hashing for data integrity.
- **Inode Management**: Utilizes inode data structures to store metadata about files and directories, including permissions, size, and data block pointers.
- **Shell Interface**: Provides a command-line interface for users to interact with the file system, executing commands like cd, ls, cat, mkdir, and append.
- **RAID5 Implementation**: Distributes parity across servers and performs efficient data recovery using XOR operations to maintain data integrity and availability.

## Usage
1. **Setup**: Clone the repository and set up the environment on both client and server machines.
2. **Configuration**: Configure server settings, including XML-RPC endpoints, block storage locations, and RAID5 parameters.
3. **Deployment**: Deploy the file system by starting the block servers and initializing the client-side interface.
4. **File Operations**: Use the shell interface to navigate directories, create files, and perform read and write operations.
5. **Fault Recovery**: Monitor and handle server failures using the repair command to reconstruct and restore data blocks.

## Contributions
Contributions to enhance the file system's functionality, improve performance, or add new features are welcome. Fork the repository, make your changes, and submit a pull request for review.

## Future Enhancements
- Expand RAID configurations to support RAID levels beyond RAID5.
- Enhance fault tolerance mechanisms for handling multiple server failures.
- Implement advanced file system features such as snapshotting and remote replication.

## License
This project is licensed under the MIT License. See LICENSE file for more details.

## Acknowledgments
This project builds upon concepts from distributed systems, fault tolerance, and file system design principles. Special thanks to contributors and open-source libraries that have supported this endeavor.

---

Feel free to explore and contribute to the Distributed Unix-like File System with RAID5! If you encounter any issues or have suggestions, please open an issue on GitHub.
